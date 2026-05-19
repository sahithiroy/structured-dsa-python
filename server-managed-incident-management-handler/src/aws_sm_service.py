import json
from typing import Optional

import boto3


class AWSSecretsManagerService:
    """
    A class to interact with AWS SecretsManager service.
    Provides methods to retrieve stack outputs and resources.
    """

    def __init__(self):
        """
        Initialize the SecretsManager client with AWS credentials.
        """
        # Create a CloudFormation client using default credentials.
        self.client = boto3.client("secretsmanager")

    def get_secret_value(self, secret_name: str) -> dict:
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            if "SecretString" in response:
                return json.loads(response["SecretString"])
            else:
                print("Secret not found or invalid format.")
                return {}
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            return {}
