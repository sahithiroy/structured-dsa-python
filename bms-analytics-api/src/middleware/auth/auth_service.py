import os
import re

import boto3
from fastapi.responses import JSONResponse

from config import AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY, SERVER_ENV
from src.middleware.aws.aws_cf_service import AWSCFService

# Configure boto3 client for Cognito Identity Provider
client = boto3.client('cognito-idp',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION)


# Function to find the user pool ID and client ID associated with a given username
def get_user_pool_and_client_id(username: str):
    """
    Finds the Cognito User Pool ID and Client ID associated with the provided username.

    Args:
        username: The username to search for in Cognito user pools.

    Returns:
        A tuple containing the User Pool ID and Client ID if found; otherwise, a JSONResponse with an error message.
    """
    try:
        # List available Cognito user pools (limited to 60 results per request)
        response = client.list_user_pools(MaxResults=60)

        # Iterate through the user pools to locate the one containing the username
        for pool in response['UserPools']:
            pool_id = pool['Id']  # Get the pool ID
            try:
                # Check if the username exists in the current user pool
                users = client.list_users(UserPoolId=pool_id, Filter=f'username = "{username}"')
                if users['Users']:  # If the user exists
                    # Retrieve the client ID associated with the user pool
                    client_id_response = client.list_user_pool_clients(UserPoolId=pool_id, MaxResults=60)
                    client_id = client_id_response['UserPoolClients'][0]['ClientId']
                    return pool_id, client_id
            except client.exceptions.UserNotFoundException:
                # If the user is not found in the current pool, continue to the next one
                continue
    except client.exceptions.ClientError as e:
        # Handle errors while listing user pools or users
        return JSONResponse(
            status_code=e.status_code,
            content={
                "statusCode": e.status_code,
                "errorCode": e.error_code,
                "message": e.description,
                "description": e.description,
                "detail": "User pool or client ID not found"
            },
        )


class AuthService:
    """
    A service class to manage authentication-related operations, such as
    retrieving Cognito User Pool details and generating formatted stack names.
    """

    def __init__(self):
        # Initialize the AWS CloudFormation service
        self.aws_cf_service = AWSCFService()

    async def get_cognito_details_based_on_user_stack(self, stack_name: str, is_super_admin: bool = False) -> tuple[
        str, str]:
        """
        Retrieves Cognito User Pool ID and Client ID based on the provided stack name.

        Args:
            stack_name: The name of the AWS CloudFormation stack.
            is_super_admin: Boolean flag to specify if the SuperAdminUserPool details should be retrieved.

        Returns:
            A tuple containing the User Pool ID and Client ID.
        """
        try:
            # Retrieve stack resources from AWS CloudFormation
            stack_resources = self.aws_cf_service.get_stack_resources(stack_name)

            # Extract the Cognito User Pool ID from the stack resources
            user_pool_id = next(
                (r["PhysicalResourceId"]
                 for r in stack_resources
                 if r["LogicalResourceId"] == ('SuperAdminUserPool' if is_super_admin else 'TenantUserPool')),
                None
            )

            # Extract the Cognito Client ID from the stack resources
            client_id = next(
                (r["PhysicalResourceId"]
                 for r in stack_resources
                 if
                 r["LogicalResourceId"] == ('SuperAdminUserPoolClient' if is_super_admin else 'TenantUserPoolClient')),
                None
            )

            return user_pool_id, client_id

        except Exception as e:
            # Handle exceptions, such as resource retrieval failures
            print(f"Error retrieving Cognito details: {str(e)}")
            raise

    def generate_formatted_string(self, str: str, replace_char: str = '_') -> str:
        """
        Formats a given string by replacing non-alphanumeric characters with a specified character.

        Args:
            str: The input string to format.
            replace_char: The character used to replace non-alphanumeric characters.

        Returns:
            The formatted string in lowercase.
        """
        return re.sub(r"[^a-zA-Z0-9]", replace_char, str).lower()

    def generate_tenant_stack_name(self, tenant_namespace: str) -> str:
        """
        Generates a formatted tenant stack name based on the provided tenant namespace.

        Args:
            tenant_namespace: The namespace for the tenant.

        Returns:
            The formatted tenant stack name.
        """
        # Define a suffix for the tenant stack name
        name_suffix = "-tenant-account"   #config_service.get("aws.cf.stack.tenantAccountSetup.nameSuffix")
        # Format the tenant namespace
        formatted_namespace = self.generate_formatted_string(str=tenant_namespace, replace_char="-")

        # Generate the stack name, limiting it to 127 characters
        stack_name = f"{formatted_namespace}-{SERVER_ENV}{name_suffix}"[:127]

        return stack_name

    def generate_super_admin_stack_name(self) -> str:
        """
        Generates the formatted stack name for the super admin.

        Returns:
            The formatted super admin stack name.
        """
        # Retrieve the environment from the server configuration
        environment = os.getenv("SERVER_ENV")

        # Define the super admin stack name
        super_admin_stack_name = "server-managed-super-admin-account-setup"  #config_service.get("aws.cf.stack.superAdminAccountSetup.name")

        # Format the final stack name
        stack_name = f"{environment}-{super_admin_stack_name}"

        return stack_name
