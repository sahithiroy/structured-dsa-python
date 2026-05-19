from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from src.api.dogs.models import Dog
from pymongo import ReturnDocument
from bson import ObjectId
from config import MONGODB_URL
from motor.motor_asyncio import AsyncIOMotorCollection
from src.api.dogs.payload import DogModelDTO, UpdateDogModel
from src.middleware.error.exceptions import ResourceNotFoundException
from motor.motor_asyncio import AsyncIOMotorClient
from src.middleware.database.schema_constants import SchemaNames, CollectionNames

class DogDao:
    def __init__(self):
        """
        Initializes the MongoDB client and connects to the database and the dogs collection.
        """
        # Create an asynchronous MongoDB client
        self.client = AsyncIOMotorClient(MONGODB_URL)
        # Access the default schema (database)
        self.db = self.client[SchemaNames.Default.value]
        # Access the dogs collection
        self.dogs_collection: AsyncIOMotorCollection = self.db[CollectionNames.Dog.value]

    async def create_dog(self, dog: DogModelDTO, owner_id: str) -> Dog:
        """
        Creates a new dog entry in the database.

        :param dog: Data transfer object containing dog details.
        :param owner_id: The ID of the owner creating the dog.
        :return: The created Dog object.
        """
        # Convert the DogModelDTO object to a dictionary, excluding unset or None values
        dog_dict: dict = dog.model_dump(exclude_none=True, exclude_unset=True)
        # Add the owner ID to the dictionary
        dog_dict["owner"] = owner_id
        # Add timestamps for creation and last update
        dog_dict["created_at"] = datetime.now(timezone.utc)
        dog_dict["updated_at"] = datetime.now(timezone.utc)
        # Generate a unique ID for the dog and add it to the dictionary
        dog_dict["id"] = str(uuid4())
        dog_dict["_id"] = dog_dict["id"]
        # Insert the dog record into the collection
        await self.dogs_collection.insert_one(dog_dict)
        # Return the created Dog object
        return Dog(**dog_dict)

    async def get_dogs(self) -> list[Dog]:
        """
        Retrieves all dog records from the database.

        :return: A list of Dog objects.
        """
        # Fetch all dog documents from the collection
        dogs = await self.dogs_collection.find().to_list(None)
        # Map each document to a Dog object
        dogs = list(map(lambda c: Dog(**c), dogs))
        return dogs

    async def get_dogs_by_owner(self, owner_id: str) -> list[Dog]:
        """
        Retrieves all dogs owned by a specific owner.

        :param owner_id: The ID of the owner.
        :return: A list of Dog objects.
        """
        # Fetch dog documents that match the owner ID
        dogs = await self.dogs_collection.find({"owner": owner_id}).to_list(None)
        # Map each document to a Dog object
        dogs = list(map(lambda c: Dog(**c), dogs))
        return dogs

    async def get_dog(self, id: str) -> Optional[Dog]:
        """
        Retrieves a specific dog by its ID.

        :param id: The ID of the dog.
        :return: The Dog object if found, otherwise None.
        """
        # Find a dog document by its ID
        dog = await self.dogs_collection.find_one({"_id": ObjectId(id)})
        if dog:
            return Dog(**dog)
        return None

    async def get_dog_by_owner(self, id: str, owner_id: str) -> Optional[Dog]:
        """
        Retrieves a specific dog by its ID and owner.

        :param id: The ID of the dog.
        :param owner_id: The ID of the owner.
        :return: The Dog object if found, otherwise None.
        """
        # Find a dog document by its ID and owner ID
        dog = await self.dogs_collection.find_one({"_id": ObjectId(id), "owner": owner_id})
        if dog:
            return Dog(**dog)
        else:
            return None

    async def update_dog(self, id: str, owner_id: str, dog: UpdateDogModel) -> Optional[Dog]:
        """
        Updates a dog's details.

        :param id: The ID of the dog.
        :param owner_id: The ID of the owner.
        :param dog: The updated dog details.
        :return: The updated Dog object if successful, otherwise None.
        """
        # Convert the UpdateDogModel object to a dictionary, excluding None values
        dog_dict = dog.model_dump(exclude_none=True)
        # Update the dog document and return the updated document
        result = await self.dogs_collection.find_one_and_update(
            {"_id": ObjectId(id), "owner": owner_id},  # Filter by ID and owner
            {"$set": dog_dict},  # Update fields
            return_document=ReturnDocument.AFTER,  # Return the updated document
        )
        if not result:
            return None
        return Dog(**result)

    async def delete_dog(self, id: str, owner_id: str) -> Dog:
        """
        Deletes a dog record by its ID and owner.

        :param id: The ID of the dog.
        :param owner_id: The ID of the owner.
        :return: The deleted Dog object.
        :raises ResourceNotFoundException: If the dog is not found.
        """
        # Fetch the dog document to ensure it exists before deleting
        dog: Dog | None = await self.get_dog_by_owner(id=id, owner_id=owner_id)
        if dog:
            # Attempt to delete the dog document
            deleted_result = await self.dogs_collection.delete_one({"_id": ObjectId(id), "owner": owner_id})
            if deleted_result.deleted_count == 0:
                # Raise an exception if deletion fails
                raise Exception("Failed to delete dog", id)
            return dog

        # Raise an exception if the dog is not found
        raise ResourceNotFoundException("Dog not found", id)
