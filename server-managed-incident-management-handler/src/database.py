import os

from pymongo import MongoClient

from aws_sm_service import AWSSecretsManagerService
from config import SECRETS_NAME


class Database:
    def __init__(self, tenant_namespace: str):
        """
        Initialize the database connection for a given tenant namespace.
        """
        mongo_url = os.getenv("MONGODB_URL", None)
        if not mongo_url:
            secrets = AWSSecretsManagerService().get_secret_value(
                secret_name=SECRETS_NAME
            )
            mongo_url = secrets.get("DEV_MONGODB_URL", "")
        self.client = MongoClient(mongo_url)
        self.db = self.client.get_database(tenant_namespace)

    def get_collection(self, collection_name: str):
        """
        Get a specific collection from the database.
        """
        return self.db[collection_name]

    def close(self):
        """
        Close the MongoDB client connection.
        """
        if self.client:
            self.client.close()

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object and close the client.
        """
        self.close()
