from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")


class MongoDB:

    def __init__(self):

        self.client = MongoClient(URL)

        self.db = None

        self.collection = None

    def connectMongoDB(self)-> None:

        try:

            self.client.admin.command('ping')

            print("Connected to MongoDB successfully!")

        except Exception as e:

            print("Error connecting to MongoDB:", e)

    def create_database(self, db_name)->None:

        print(self.client.list_database_names())

        self.db = self.client[db_name]

        if db_name not in self.client.list_database_names():

            print("Database created successfully")

        else:

            print("Database already exists")

    def create_collection(self, collection_name)-> None:

        print(self.db.list_collection_names())

        self.collection = self.db[collection_name]

        if collection_name not in self.db.list_collection_names():

            print("Collection created successfully")

        else:

            print("Collection already exists")

    def insert_one(self, document)-> dict:

        if self.collection is not None:

            result = self.collection.insert_one(document)

            print("Inserted ID:", result.inserted_id)

            return result

        else:

            print("Collection not found")