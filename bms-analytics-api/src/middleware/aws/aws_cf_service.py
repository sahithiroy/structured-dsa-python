import boto3

class AWSCFService:
    """
    A class to interact with AWS CloudFormation service.
    Provides methods to retrieve stack outputs and resources.
    """

    def __init__(self, **credentials):
        """
        Initialize the CloudFormation client with AWS credentials.
        If credentials are provided, temporary credentials are used to authenticate.
        Otherwise, the default AWS credentials from the environment or configuration file are used.

        Args:
            credentials (dict): A dictionary containing AWS credentials:
                - AccessKeyId: AWS access key ID.
                - SecretAccessKey: AWS secret access key.
                - SessionToken: AWS session token (for temporary credentials).
                - RegionName: AWS region name.
        """
        if credentials:
            # Create a CloudFormation client using the provided credentials.
            self.client = boto3.client(
                "cloudformation",
                aws_access_key_id=credentials.get("AccessKeyId", ""),
                aws_secret_access_key=credentials.get("SecretAccessKey", ""),
                aws_session_token=credentials.get("SessionToken", ""),
                region_name=credentials.get("RegionName", ""),
            )
        else:
            # Create a CloudFormation client using default credentials.
            self.client = boto3.client("cloudformation")

    def get_stack_outputs(self, stack_name: str):
        """
        Retrieve the outputs of a CloudFormation stack.

        Args:
            stack_name (str): The name of the CloudFormation stack.

        Returns:
            list: A list of outputs from the specified stack.
                  Each output contains a dictionary with details like `OutputKey`, `OutputValue`, etc.
                  Returns an empty list if an error occurs.
        """
        try:
            # Describe the stack to get its outputs.
            response = self.client.describe_stacks(StackName=stack_name)
            # Extract the outputs from the first stack in the response.
            outputs = response["Stacks"][0]["Outputs"]
            return outputs
        except Exception as e:
            # Print an error message and return an empty list in case of an exception.
            print(f"Error describing stack outputs: {e}")
            return []

    def get_stack_resources(self, stack_name: str):
        """
        Retrieve the resources of a CloudFormation stack.

        Args:
            stack_name (str): The name of the CloudFormation stack.

        Returns:
            list: A list of resources in the specified stack.
                  Each resource contains a dictionary with details like `LogicalResourceId`, `ResourceType`, etc.
                  Returns an empty list if an error occurs.
        """
        try:
            # Describe the stack to get its resources.
            response = self.client.describe_stack_resources(StackName=stack_name)
            # Extract the list of resources from the response.
            return response["StackResources"]
        except Exception as e:
            # Print an error message and return an empty list in case of an exception.
            print(f"Error describing stack resources: {e}")
            return []
