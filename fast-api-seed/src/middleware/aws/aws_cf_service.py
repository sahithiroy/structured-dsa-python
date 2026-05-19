import boto3


class AWSCFService:
    """
    A AWS cloud formation service class
    """

    def __init__(self, **credentials):
        # Assume the role and get temporary credentials
        if credentials:
            self.client = boto3.client(
                "cloudformation",
                aws_access_key_id=credentials.get("AccessKeyId", ""),
                aws_secret_access_key=credentials.get("SecretAccessKey", ""),
                aws_session_token=credentials.get("SessionToken", ""),
                region_name=credentials.get("RegionName", ""),
            )
        else:
            self.client = boto3.client("cloudformation")

    def get_stack_outputs(self, stack_name: str):
        try:
            response = self.client.describe_stacks(StackName=stack_name)
            outputs = response["Stacks"][0]["Outputs"]
            return outputs
        except Exception as e:
            print(f"Error describing stack outputs: {e}")
            return []

    def get_stack_resources(self, stack_name: str):
        try:
            response = self.client.describe_stack_resources(StackName=stack_name)
            return response["StackResources"]
        except Exception as e:
            print(f"Error describing stack resources: {e}")
            return []
