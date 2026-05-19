from pymongo import MongoClient

from config import MONGODB_URL

class Database:
    def __init__(self, tenant_namespace: str):
        """
        Initialize the database connection for a given tenant namespace.
        """
        self.client = MongoClient(MONGODB_URL)
        self.db = self.client.get_database(tenant_namespace)

    def get_collection(self, collection_name: str):
        """
        Get a specific collection from the database.
        """
        return self.db[collection_name]
