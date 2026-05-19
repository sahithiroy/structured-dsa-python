from src.api.dogs.dao import DogDao
from src.api.dogs.payload import DogModelDTO, UpdateDogModel
from src.api.dogs.models import Dog
from src.middleware.error.exceptions import ResourceNotFoundException

class DogService:
    def __init__(self):
        """
        Initializes the DogService with an instance of DogDao for database interactions.
        """
        # Instantiate the DogDao for database access
        self.dao = DogDao()

    # Create a new dog entry
    async def create_dog(self, dog: DogModelDTO, owner_id: str) -> Dog:
        """
        Creates a new dog entry for a given owner.

        :param dog: The dog details provided as a DogModelDTO.
        :param owner_id: The ID of the owner creating the dog.
        :return: The created Dog object.
        """
        # Call the DAO method to create a dog and return the result
        return await self.dao.create_dog(dog=dog, owner_id=owner_id)

    async def list_dogs(self, owner_id: str):
        """
        Lists all dogs owned by a specific owner.

        :param owner_id: The ID of the owner.
        :return: A list of Dog objects owned by the owner.
        """
        # Retrieve the list of dogs for the given owner from the DAO
        return await self.dao.get_dogs_by_owner(owner_id=owner_id)

    async def show_dog(self, id: str, owner_id: str) -> Dog:
        """
        Retrieves details of a specific dog owned by an owner.

        :param id: The ID of the dog.
        :param owner_id: The ID of the owner.
        :return: The Dog object if found.
        :raises ResourceNotFoundException: If the dog is not found.
        """
        # Fetch the dog details by its ID and owner ID using the DAO
        dog = await self.dao.get_dog_by_owner(id, owner_id=owner_id)
        # Raise an exception if the dog is not found
        if not dog:
            raise ResourceNotFoundException("Dog not found", id)
        return dog

    # Update a specific dog entry
    async def update_dog(self, id: str, owner_id: str, dog: UpdateDogModel) -> Dog:
        """
        Updates the details of a specific dog.

        :param id: The ID of the dog to be updated.
        :param owner_id: The ID of the owner of the dog.
        :param dog: The updated dog details as an UpdateDogModel.
        :return: The updated Dog object.
        :raises ResourceNotFoundException: If the dog is not found.
        """
        # Call the DAO method to update the dog details
        updated_dog = await self.dao.update_dog(id, owner_id=owner_id, dog=dog)
        # Raise an exception if the dog is not found
        if not updated_dog:
            raise ResourceNotFoundException("Dog not found", id)
        return updated_dog

    # Delete a specific dog entry
    async def delete_dog(self, id: str, owner_id: str) -> Dog:
        """
        Deletes a specific dog entry.

        :param id: The ID of the dog to be deleted.
        :param owner_id: The ID of the owner of the dog.
        :return: The deleted Dog object.
        """
        # First, fetch the dog details to ensure it exists
        ex_dog = await self.show_dog(id=id, owner_id=owner_id)
        # Call the DAO method to delete the dog
        await self.dao.delete_dog(id=id, owner_id=owner_id)
        # Return the deleted Dog object
        return ex_dog




