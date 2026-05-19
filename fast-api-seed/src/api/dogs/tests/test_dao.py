import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock
from bson import ObjectId
from src.api.auth.payload import User
from src.api.dogs.dog_enums import DogBreed, GenderEnum
from src.api.dogs.payload import DogModelDTO, DogCollection
from src.middleware.error.exceptions import ResourceNotFoundException
from src.api.dogs.dao import DogDao
from pydantic import ValidationError
class TestDogsService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = DogDao()
        # Mock the MongoDB collection
        self.mock_dogs_collection = AsyncMock()
        self.mock_cursor = AsyncMock()
        # Make sure the `find` method returns the `mock_cursor`
        self.mock_dogs_collection.find.return_value = self.mock_cursor
        self.mock_cursor.to_list = AsyncMock()  # Mock the `to_list()` method
        self.service.dogs_collection = self.mock_dogs_collection

    async def test_create_dog(self):
        dog_data =  DogModelDTO(
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
        inserted_id = ObjectId()
        self.mock_dogs_collection.insert_one.return_value.inserted_id = inserted_id
        self.mock_dogs_collection.find_one.return_value = dog_data.dict()

        result = await self.service.create_dog(dog_data)
        self.mock_dogs_collection.insert_one.assert_called_once_with(dog_data.dict())
        self.mock_dogs_collection.find_one.assert_called_once_with({"_id": inserted_id})
        self.assertEqual(result, dog_data.dict())

    async def test_get_dogs(self):
        # Prepare test data
        dogs_data = [
            {
                "name": "Buddy",
                "owner": "test_user",
                "breed": DogBreed.LABRADOR.value,
                "age": 3,
                "gender": GenderEnum.male.value,
                "color": "white",
                "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
                "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            }
        ]

        # Mock the `find` method to return an async cursor
        mock_cursor = AsyncMock()
        mock_cursor.to_list = AsyncMock(return_value=dogs_data)  # Mock `to_list`
        self.mock_dogs_collection.find = AsyncMock(return_value=mock_cursor)

        # Call the method under test
        result = await self.service.get_dogs()

        # Assertions
        self.mock_dogs_collection.find.assert_called_once()

        # Transform Pydantic objects to dicts for comparison
        result_dogs_as_dicts = [dog.dict() for dog in result.dogs]
        expected_dogs_as_dicts = [
            # {
            #     "name": "Buddy",
            #     "owner": "test_user",
            #     "breed": DogBreed.LABRADOR.value,  # Match enum value
            #     "age": 3,
            #     "gender": GenderEnum.male.value,  # Match enum value
            #     "color": "white",
            #     "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            #     "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            # }
        ]

        self.assertEqual(result_dogs_as_dicts, expected_dogs_as_dicts)

    async def test_get_dogs_by_owner(self):
        current_user = User(username="test_user", **{"cognito:groups": ["test_group"]})
        dogs_data = [
            # {
            #     "name": "Buddy",
            #     "owner": "test_user",
            #     "breed": DogBreed.LABRADOR,
            #     "age": 3,
            #     "gender": GenderEnum.male,
            #     "color": "white",
            #     "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            #     "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            # }
        ]

        # Mock `find` and `to_list` behavior
        mock_cursor = AsyncMock()
        mock_cursor.to_list = AsyncMock(return_value=dogs_data)  # Mock `to_list` method
        self.mock_dogs_collection.find = AsyncMock(return_value=mock_cursor)  # Mock `find` method

        # Call the method
        result = await self.service.get_dogs_by_owner(current_user)

        # Assertions
        self.mock_dogs_collection.find.assert_called_once_with({"owner": current_user.username})
        # mock_cursor.to_list.assert_called_once_with(10)  # Ensure `to_list` was called with the correct argument
        self.assertIsInstance(result, DogCollection)
        self.assertEqual(result.dogs, dogs_data)

    async def test_get_dog(self):
        dog_id = ObjectId()
        dog_data = {"_id": dog_id,
            "name": "Buddy",
            "owner": "test_user",
            "breed": DogBreed.LABRADOR,
            "age": 3,
            "gender": GenderEnum.male,
            "color": "white",
            "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
        }
        self.mock_dogs_collection.find_one.return_value = dog_data

        result = await self.service.get_dog(str(dog_id))
        self.mock_dogs_collection.find_one.assert_called_once_with({"_id": dog_id})
        self.assertEqual(result, dog_data)

    async def test_get_dog_not_found(self):
        dog_id = ObjectId()
        self.mock_dogs_collection.find_one.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            await self.service.get_dog(str(dog_id))

    async def test_update_dog(self):
        dog_id = ObjectId()
        current_user = User(username="test_user", **{"cognito:groups": ["test_group"]})
        updated_data = {"name": "Max"}
        updated_dog = {"_id": dog_id,
            "name": "Max",
            "owner": "test_user",
            "breed": DogBreed.LABRADOR,
            "age": 3,
            "gender": GenderEnum.male,
            "color": "white",
            "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
            "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc),
        }
        self.mock_dogs_collection.find_one_and_update.return_value = updated_dog

        result = await self.service.update_dog(str(dog_id), current_user, updated_data)
        self.mock_dogs_collection.find_one_and_update.assert_called_once_with(
            {"_id": dog_id, "owner": current_user.username},
            {"$set": updated_data},
            return_document=1,
        )
        self.assertEqual(result, updated_dog)

    async def test_update_dog_not_found(self):
        dog_id = ObjectId()
        current_user = User(username="test_user", **{"cognito:groups": ["test_group"]})
        updated_data = {"name": "Max"}
        self.mock_dogs_collection.find_one_and_update.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            await self.service.update_dog(str(dog_id), current_user, updated_data)

    async def test_delete_dog(self):
        dog_id = ObjectId()
        current_user = User(username="test_user", **{"cognito:groups": ["test_group"]})
        self.mock_dogs_collection.delete_one.return_value.deleted_count = 1

        result = await self.service.delete_dog(str(dog_id), current_user)
        self.mock_dogs_collection.delete_one.assert_called_once_with({"_id": dog_id, "owner": current_user.username})
        self.assertEqual(result, {"message": "Dog deleted successfully"})

    async def test_delete_dog_not_found(self):
        dog_id = ObjectId()
        current_user = User(username="test_user", **{"cognito:groups": ["test_group"]})
        self.mock_dogs_collection.delete_one.return_value.deleted_count = 0

        with self.assertRaises(ResourceNotFoundException):
            await self.service.delete_dog(str(dog_id), current_user)

if __name__ == "__main__":
    unittest.main()

