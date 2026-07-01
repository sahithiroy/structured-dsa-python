from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")


class MongoDB:

    def __init__(self):
        self.client = AsyncIOMotorClient(URL)
        self.db = None
        self.collection = None

    async def connectMongoDB(self):

        try:
            await self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")

        except Exception as e:
            print("Error connecting to MongoDB:", e)

    async def create_database(self, db_name):

        self.db = self.client[db_name]

        print(f"Using database: {db_name}")

    async def create_collection(self, collection_name):

        self.collection = self.db[collection_name]

        print(f"Using collection: {collection_name}")

    async def insert_one(self, document):

        print("Collection:", self.collection)

        if self.collection is not None:

            result = await self.collection.insert_one(document)

            return result

        else:
            print("Collection not found")
            