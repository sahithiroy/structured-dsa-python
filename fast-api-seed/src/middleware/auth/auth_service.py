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
    try:
        # List available Cognito user pools (up to 60)
        response = client.list_user_pools(MaxResults=60)
        # Iterate through the user pools to find the one containing the given username
        for pool in response['UserPools']:
            pool_id = pool['Id']
            try:
                # Check if the username exists in the current user pool
                users = client.list_users(UserPoolId=pool_id, Filter=f'username = "{username}"')
                if users['Users']:
                    # If user is found, retrieve the client ID associated with the user pool
                    client_id_response = client.list_user_pool_clients(UserPoolId=pool_id, MaxResults=60)
                    client_id = client_id_response['UserPoolClients'][0]['ClientId']
                    return pool_id, client_id
            except client.exceptions.UserNotFoundException:
                # Continue searching if the user is not found in the current pool
                continue
    except client.exceptions.ClientError as e:
        # Handle errors that occur while listing user pools or users
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
    def __init__(self):
        self.aws_cf_service = AWSCFService()

    async def get_cognito_details_based_on_user_stack(self, stack_name: str, is_super_admin: bool = False) -> tuple[str,str]:
        """
        Retrieves Cognito User Pool ID and Client ID based on the provided stack name.
        :param stack_name: The name of the AWS CloudFormation stack.
        :param is_super_admin: If True, retrieves details for the SuperAdminUserPool.
                                Otherwise, retrieves details for the TenantUserPool.
        :return: A dictionary containing the UserPoolId and ClientId.
        """
        try:
            # Get the user stack resources
            stack_resources = self.aws_cf_service.get_stack_resources(stack_name)
            # Extract the cognito details from the stack resources
            user_pool_id = next(
                (r["PhysicalResourceId"]
                 for r in stack_resources
                 if r["LogicalResourceId"] == ('SuperAdminUserPool' if is_super_admin else 'TenantUserPool')),
                None
            )
            client_id = next(
                (r["PhysicalResourceId"]
                 for r in stack_resources
                 if r["LogicalResourceId"] == ('SuperAdminUserPoolClient' if is_super_admin else 'TenantUserPoolClient')),
                None
            )

            return user_pool_id, client_id

        except Exception as e:
            # Handle exceptions gracefully (e.g., log, raise a custom exception)
            print(f"Error retrieving Cognito details: {str(e)}")
            raise

    def generate_formatted_string(self, str: str, replace_char: str = '_') -> str:
        return re.sub(r"[^a-zA-Z0-9]", replace_char, str).lower()

    def generate_tenant_stack_name(self, tenant_namespace: str) -> str:
        """
        Generates the tenant stack name based on the provided tenant namespace.

        Args:
          tenant_namespace: The namespace for the tenant.

        Returns:
          The formatted tenant stack name.
        """

        # Retrieve environment variable and configuration service value
        # todo keep it in config
        name_suffix = "-tenant-account" #config_service.get("aws.cf.stack.tenantAccountSetup.nameSuffix")
        # Format the stack name
        formatted_namespace = self.generate_formatted_string(str=tenant_namespace, replace_char="-")
        stack_name = f"{formatted_namespace}-{SERVER_ENV}{name_suffix}"[:127]
        return stack_name

    def generate_super_admin_stack_name(self) -> str:
        """
        Generates the super admin stack name.

        Returns:
          The formatted super admin stack name.
        """

        # Retrieve environment variable and configuration service value
        environment = os.getenv("SERVER_ENV")
        # todo keep it in config
        super_admin_stack_name = "server-managed-super-admin-account-setup" #config_service.get("aws.cf.stack.superAdminAccountSetup.name")

        # Format the stack name
        stack_name = f"{environment}-{super_admin_stack_name}"

        return stack_name
