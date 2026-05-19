import unittest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone
from fastapi import HTTPException

from src.api.dogs.dog_enums import DogBreed, GenderEnum
from src.api.dogs.service import DogController
from src.api.dogs.models import DogModelDTO
from src.api.auth.models import User
from src.middleware.error.exceptions import ResourceNotFoundException


class TestDogController(unittest.TestCase):

    def setUp(self):
        # Initialize the DogController and mock the dependencies
        self.controller = DogController()

        # Mock the DogsService
        self.controller.dogs_service = MagicMock()

        # Mock a sample User
        self.mock_user = {
            "username": "test_user",
            "role": "Admin"
        }

        # Mock a DogModelDTO instance
        self.mock_dog =DogModelDTO(
                id=None,
                name="Buddy",
                owner="test_user",
                breed=DogBreed.LABRADOR,
                age=3,
                gender=GenderEnum.male,
                color="white",
                created_at=datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
                updated_at=datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            )

    # Test create_dog method
    async def test_create_dog(self):
        # Prepare the dog_dict to match what the controller would return
        dog_dict = {
                "name": "Buddy",
                "owner": "test_user",
                "breed": DogBreed.LABRADOR,
                "age": 3,
                "gender": GenderEnum.male,
                "color": "white",
                "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
                "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            }

        # Mock the creates_dog method to return the same dog_dict
        self.controller.dogs_service.creates_dog = AsyncMock(return_value=dog_dict)

        # Call the controller method
        result = await self.controller.create_dog(self.mock_dog, self.mock_user)

        # Assert that the method returns the expected dog_dict
        self.assertEqual(result, dog_dict)
        self.controller.dogs_service.creates_dog.assert_called_once_with(dog_dict)

    # Test list_dogs method for AccountAdmin role
    async def test_list_dogs_account_admin(self):
        # Mock the get_dogs method
        self.controller.dogs_service.get_dogs = AsyncMock(return_value=[])

        # Call the controller method
        result = await self.controller.list_dogs(self.mock_user)

        # Assert that the get_dogs method was called
        self.controller.dogs_service.get_dogs.assert_called_once()
        self.assertEqual(result, [])

    # Test list_dogs method for regular user (owner)
    async def test_list_dogs_owner(self):
        # Mock the get_dogs_by_owner method
        self.controller.dogs_service.get_dogs_by_owner = AsyncMock(return_value=[])

        # Mock user with role other than AccountAdmin
        self.mock_user["role"] = "User"

        # Call the controller method
        result = await self.controller.list_dogs(self.mock_user)

        # Assert that the get_dogs_by_owner method was called
        self.controller.dogs_service.get_dogs_by_owner.assert_called_once_with(self.mock_user)
        self.assertEqual(result, [])

    # Test show_dog method for AccountAdmin role
    async def test_show_dog_account_admin(self):
        # Mock the get_dog method
        dog_data = {
            "name": "Buddy",
            "owner": "test_user",
            "breed": "Labrador",
            "age": 3,
            "color": "white"
        }
        self.controller.dogs_service.get_dog = AsyncMock(return_value=dog_data)

        # Call the controller method
        result = await self.controller.show_dog("dog_id", self.mock_user)

        # Assert that the get_dog method was called
        self.controller.dogs_service.get_dog.assert_called_once_with("dog_id")
        self.assertEqual(result, dog_data)

    # Test show_dog method for regular user (owner)
    async def test_show_dog_owner(self):
        # Mock the get_dog_by_owner method
        dog_data = {
            "name": "Buddy",
            "owner": "test_user",
            "breed": "Labrador",
            "age": 3,
            "color": "white"
        }
        self.controller.dogs_service.get_dog_by_owner = AsyncMock(return_value=dog_data)

        # Call the controller method
        result = await self.controller.show_dog("dog_id", self.mock_user)

        # Assert that the get_dog_by_owner method was called
        self.controller.dogs_service.get_dog_by_owner.assert_called_once_with("dog_id", self.mock_user)
        self.assertEqual(result, dog_data)

    # Test update_dog method
    async def test_update_dog(self):
        update_data = {"name": "Max"}
        self.mock_dog.model_dump = MagicMock(return_value=update_data)

        # Mock the updates_dog method to return the updated data
        self.controller.dogs_service.updates_dog = AsyncMock(return_value=update_data)

        # Call the controller method
        result = await self.controller.update_dog("dog_id", self.mock_user, self.mock_dog)

        # Assert the updated data
        self.assertEqual(result, update_data)
        self.controller.dogs_service.updates_dog.assert_called_once_with("dog_id", self.mock_user, update_data)

    # Test update_dog method when no updates are made
    async def test_update_dog_no_changes(self):
        self.mock_dog.model_dump = MagicMock(return_value={})

        # Call the controller method
        result = await self.controller.update_dog("dog_id", self.mock_user, self.mock_dog)

        # Assert that ResourceNotFoundException is raised
        self.assertIsInstance(result, ResourceNotFoundException)

    # Test delete_dog method
    async def test_delete_dog(self):
        # Mock the deletes_dog method to return a mock result
        delete_result = MagicMock()
        delete_result.deleted_count = 1
        self.controller.dogs_service.deletes_dog = AsyncMock(return_value=delete_result)

        # Call the controller method
        result = await self.controller.delete_dog("dog_id", self.mock_user)

        # Assert that the dog was deleted successfully
        self.assertEqual(result.status_code, 200)
        self.controller.dogs_service.deletes_dog.assert_called_once_with("dog_id", self.mock_user)

    # Test delete_dog method when dog not found
    async def test_delete_dog_not_found(self):
        # Mock the deletes_dog method to return a mock result with no deletions
        delete_result = MagicMock()
        delete_result.deleted_count = 0
        self.controller.dogs_service.deletes_dog = AsyncMock(return_value=delete_result)

        # Call the controller method
        result = await self.controller.delete_dog("dog_id", self.mock_user)

        # Assert that ResourceNotFoundException is raised
        self.assertIsInstance(result, ResourceNotFoundException)


if __name__ == "__main__":
    unittest.main()
