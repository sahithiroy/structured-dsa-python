from src.api.cats.dao import CatDao
from src.api.cats.models import Cat
from src.api.cats.payload import CreateCatDto, UpdateCatDto
from src.middleware.error.exceptions import ResourceNotFoundException


class CatService:
    """
    Service layer for managing cat-related business logic.
    This layer acts as an intermediary between the API and the DAO (Data Access Object).
    """

    def __init__(self):
        """
        Initialize the CatService with a DAO instance.
        """
        self.dao = CatDao()

    async def create_cat(self, cat: CreateCatDto, owner_id: str) -> Cat:
        """
        Create a new cat.

        :param cat: The CreateCatDto containing the cat details.
        :param owner_id: The ID of the user who owns the cat.
        :return: The newly created Cat object.
        """
        # Delegate the creation logic to the DAO
        return await self.dao.create_cat(cat=cat, owner_id=owner_id)

    async def list_cats(self, owner_id: str) -> list[Cat]:
        """
        Retrieve all cats owned by a specific user.

        :param owner_id: The ID of the user who owns the cats.
        :return: A list of Cat objects belonging to the user.
        """
        # Fetch cats owned by the specified user
        return await self.dao.get_cats_by_owner(owner_id=owner_id)

    async def show_cat(self, id: str, owner_id: str) -> Cat:
        """
        Retrieve a specific cat by its ID and owner's ID.

        :param id: The unique ID of the cat.
        :param owner_id: The ID of the owner.
        :return: The Cat object if found.
        :raises ResourceNotFoundException: If the cat is not found.
        """
        # Fetch the cat using the DAO
        cat = await self.dao.get_cat_by_owner(id=id, owner_id=owner_id)
        if not cat:
            # Raise an exception if the cat does not exist
            raise ResourceNotFoundException("Cat not found", id)
        return cat

    async def update_cat(self, id: str, owner_id: str, cat: UpdateCatDto) -> Cat:
        """
        Update the details of an existing cat.

        :param id: The unique ID of the cat.
        :param owner_id: The ID of the owner.
        :param cat: The UpdateCatDto containing updated cat details.
        :return: The updated Cat object.
        :raises ResourceNotFoundException: If the cat is not found.
        """
        # Delegate the update logic to the DAO
        updated_cat = await self.dao.update_cat(id=id, owner_id=owner_id, cat=cat)
        if not updated_cat:
            # Raise an exception if the update fails (e.g., cat not found)
            raise ResourceNotFoundException("Cat not found", id)
        return updated_cat

    async def delete_cat(self, id: str, owner_id: str) -> Cat:
        """
        Delete a cat by its ID and owner's ID.

        :param id: The unique ID of the cat.
        :param owner_id: The ID of the owner.
        :return: The deleted Cat object.
        :raises ResourceNotFoundException: If the cat is not found.
        """
        # First, ensure the cat exists by fetching it
        ex_cat = await self.show_cat(id=id, owner_id=owner_id)
        # Delegate the deletion logic to the DAO
        await self.dao.delete_cat(id=id, owner_id=owner_id)
        # Return the deleted cat object
        return ex_cat
