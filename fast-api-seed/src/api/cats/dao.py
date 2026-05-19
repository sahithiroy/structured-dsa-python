from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ReturnDocument

from config import MONGODB_URL
from src.api.cats.models import Cat
from src.api.cats.payload import CreateCatDto, UpdateCatDto
from src.middleware.database.schema_constants import SchemaNames, CollectionNames
from src.middleware.error.exceptions import ResourceNotFoundException


class CatDao:
    """
    Data Access Object (DAO) class for managing cat data in MongoDB.
    """

    def __init__(self):
        """
        Initialize the MongoDB client and create the cats collection.
        """
        # Establish a connection to the MongoDB database
        self.client = AsyncIOMotorClient(MONGODB_URL)
        # Access the default schema/database
        self.db = self.client[SchemaNames.Default.value]
        # Define the cats collection
        self.cats_collection: AsyncIOMotorCollection = self.db[CollectionNames.Cat.value]

    async def create_cat(self, cat: CreateCatDto, owner_id: str) -> Cat:
        """
        Create a new cat document in the database.

        :param cat: The CreateCatDto containing the cat details.
        :param owner_id: The ID of the user who owns the cat.
        :return: The newly created Cat object.
        """
        # Convert the DTO to a dictionary and add metadata
        cat_dict: dict = cat.model_dump(exclude_none=True, exclude_unset=True)
        cat_dict["owner"] = owner_id
        cat_dict["created_at"] = datetime.now(timezone.utc)
        cat_dict["updated_at"] = datetime.now(timezone.utc)
        cat_dict["id"] = str(uuid4())  # Generate a unique ID
        cat_dict["_id"] = cat_dict["id"]  # MongoDB-specific identifier
        # Insert the new cat document into the database
        await self.cats_collection.insert_one(cat_dict)
        # Return the created Cat object
        return Cat(**cat_dict)

    async def get_cats(self) -> list[Cat]:
        """
        Retrieve all cats from the database.

        :return: A list of Cat objects.
        """
        # Fetch all cat documents and convert them into Cat objects
        cats = await self.cats_collection.find().to_list(10)  # Limit results to 10
        cats = list(map(lambda c: Cat(**c), cats))
        return cats

    async def get_cats_by_owner(self, owner_id: str) -> list[Cat]:
        """
        Retrieve all cats owned by a specific user.

        :param owner_id: The ID of the owner.
        :return: A list of Cat objects belonging to the owner.
        """
        # Query the database for cats owned by the specified user
        cats = await self.cats_collection.find({"owner": owner_id}).to_list(None)
        cats = list(map(lambda c: Cat(**c), cats))
        return cats

    async def get_cat(self, id: str) -> Optional[Cat]:
        """
        Retrieve a single cat by its ID.

        :param id: The unique ID of the cat.
        :return: The Cat object if found, otherwise None.
        """
        # Query the database for a cat with the specified ID
        cat = await self.cats_collection.find_one({"_id": id})
        if cat:
            return Cat(**cat)
        return None

    async def get_cat_by_owner(self, id: str, owner_id: str) -> Optional[Cat]:
        """
        Retrieve a single cat by its ID and owner ID.

        :param id: The unique ID of the cat.
        :param owner_id: The ID of the owner.
        :return: The Cat object if found, otherwise None.
        """
        # Query the database for a cat with the specified ID and owner ID
        cat = await self.cats_collection.find_one(
            {"_id": id, "owner": owner_id}
        )
        if cat:
            return Cat(**cat)
        else:
            return None

    async def update_cat(self, id: str, owner_id: str, cat: UpdateCatDto) -> Optional[Cat]:
        """
        Update a cat's details.

        :param id: The unique ID of the cat.
        :param owner_id: The ID of the owner.
        :param cat: The UpdateCatDto containing updated cat details.
        :return: The updated Cat object if successful, otherwise None.
        """
        # Convert the DTO to a dictionary and update the cat document
        cat_dict = cat.model_dump(exclude_none=True)
        result = await self.cats_collection.find_one_and_update(
            {"_id": id, "owner": owner_id},  # Query by ID and owner
            {"$set": cat_dict},  # Update fields
            return_document=ReturnDocument.AFTER,  # Return the updated document
        )
        if not result:
            return None
        return Cat(**result)

    async def delete_cat(self, id: str, owner_id: str) -> Cat:
        """
        Delete a cat by its ID and owner ID.

        :param id: The unique ID of the cat.
        :param owner_id: The ID of the owner.
        :return: The deleted Cat object.
        :raises ResourceNotFoundException: If the cat is not found.
        """
        # Fetch the cat to ensure it exists
        cat: Cat | None = await self.get_cat_by_owner(id=id, owner_id=owner_id)
        if cat:
            # Delete the cat document
            delete_result = await self.cats_collection.delete_one(
                {"_id": id, "owner": owner_id}
            )
            if delete_result.deleted_count == 0:
                raise Exception("Failed to delete cat", id)
            return cat
        # Raise an exception if the cat is not found
        raise ResourceNotFoundException("Cat not found", id)
