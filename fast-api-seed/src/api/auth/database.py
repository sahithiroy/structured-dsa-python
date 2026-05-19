from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the MongoDB connection URL
MONGODB_URL = os.getenv("MONGODB_URL")

# Create an asynchronous MongoDB client using the connection URL and access the "cats_db" database
client = AsyncIOMotorClient(MONGODB_URL)
db = client["cats_db"]

users_collection = db["users"]