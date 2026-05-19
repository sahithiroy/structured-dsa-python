# import unittest
# from datetime import datetime, timezone
#
# from fastapi.testclient import TestClient
#
# from src.api.common_enums import Role
# from src.api.dogs.router import admin_router,user_router  # assuming the FastAPI app is imported from `src.main`
# from unittest.mock import patch
# from config import AUTH_TOKEN
# from src.api.dogs.dog_enums import DogBreed, GenderEnum
# from src.api.dogs.models import DogModelDTO
# from src.api.auth.payload import User
#
#
# class TestDogRoutes(unittest.TestCase):
#     def setUp(self):
#         """Set up the test client and common mock data."""
#         self.client = TestClient(admin_router)
#
#         # Sample user data (mock)
#         self.admin_user = User(username="test_user", **{"cognito:groups": [Role.admin.value]})
#         self.normal_user = User(username="test_user", **{"cognito:groups": [Role.user.value]})
#         self.headers = {"Authorization": "Bearer " + AUTH_TOKEN}  # Corrected to be a dictionary
#
#         # Sample dog data
#         self.dog_data = {
#             "name": "Buddy",
#             "owner": "test_user",
#             "breed": DogBreed.LABRADOR.value,
#             "age": 3,
#             "gender": GenderEnum.male.value,
#             "color": "white",
#             "created_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc).isoformat(),
#             "updated_at": datetime(2025, 1, 17, 5, 57, 39, 178374, tzinfo=timezone.utc).isoformat(),
#         }
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     @patch("src.middleware.auth.aws_auth_strategy.AWSAuthStrategy.__call__")  # Mock the JWT decoding
#     def test_admin_create_dog(self, mock_jwt_decode,mock_role_checker):
#         """Test for creating a dog by Admin."""
#         # Mocking JWT decoding to return a valid payload
#         mock_jwt_decode.return_value = {"username": "test_user", "roles": [Role.admin.value]}
#         mock_role_checker.return_value = self.admin_user
#         response = self.client.post("/dogs", headers=self.headers, json=self.dog_data)
#
#         assert response.status_code == 200
#         assert "name" in response.json()
#         assert response.json()["name"] == "Buddy"
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_user_create_dog(self, mock_role_checker):
#         self.client = TestClient(user_router)
#         """Test for creating a dog by normal User."""
#         mock_role_checker.return_value = self.normal_user
#         response = self.client.post("/dogs", headers=self.headers, json=self.dog_data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("name", response.json())
#         self.assertEqual(response.json()["name"], "Buddy")
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_admin_get_dog(self, mock_role_checker):
#         """Test for retrieving a dog's details by Admin."""
#         mock_role_checker.return_value = self.admin_user
#         dog_id = "some_dog_id"
#         response = self.client.get(f"/dogs/{dog_id}", headers=self.headers)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("name", response.json())
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_user_get_dog(self, mock_role_checker):
#         """Test for retrieving a dog's details by User."""
#         self.client = TestClient(user_router)
#         mock_role_checker.return_value = self.normal_user
#         dog_id = "some_dog_id"
#         response = self.client.get(f"/dogs/{dog_id}", headers=self.headers)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("name", response.json())
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_admin_update_dog(self, mock_role_checker):
#         """Test for updating a dog's details by Admin."""
#         mock_role_checker.return_value = self.admin_user
#         dog_id = "some_dog_id"
#         update_data = {"age": 4}  # Updating age of the dog
#         response = self.client.put(f"/dogs/{dog_id}", headers=self.headers, json=update_data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("age", response.json())
#         self.assertEqual(response.json()["age"], 4)
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_user_update_dog(self, mock_role_checker):
#         """Test for updating a dog's details by User."""
#         self.client = TestClient(user_router)
#         mock_role_checker.return_value = self.normal_user
#         dog_id = "some_dog_id"
#         update_data = {"age": 4}  # Updating age of the dog
#         response = self.client.put(f"/dogs/{dog_id}", headers=self.headers, json=update_data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("age", response.json())
#         self.assertEqual(response.json()["age"], 4)
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_admin_delete_dog(self, mock_role_checker):
#         """Test for deleting a dog by Admin."""
#         mock_role_checker.return_value = self.admin_user
#         dog_id = "some_dog_id"
#         response = self.client.delete(f"/dogs/{dog_id}", headers=self.headers)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("detail", response.json())
#         self.assertEqual(response.json()["detail"], "Dog deleted successfully")
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_user_delete_dog(self, mock_role_checker):
#         """Test for deleting a dog by User."""
#         self.client = TestClient(user_router)
#         mock_role_checker.return_value = self.normal_user
#         dog_id = "some_dog_id"
#         response = self.client.delete(f"/dogs/{dog_id}", headers=self.headers)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("detail", response.json())
#         self.assertEqual(response.json()["detail"], "Dog deleted successfully")
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_admin_list_dogs(self, mock_role_checker):
#         """Test for listing all dogs by Admin."""
#         mock_role_checker.return_value = self.admin_user
#         response = self.client.get("/dogs", headers=self.headers)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("dogs", response.json())
#
#     @patch("src.middleware.auth.aws_auth_strategy.RoleChecker.__call__")
#     def test_user_list_dogs(self, mock_role_checker):
#         """Test for listing all dogs by User."""
#         self.client = TestClient(user_router)
#         mock_role_checker.return_value = self.normal_user
#         response = self.client.get("/dogs", headers=self.headers)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("dogs", response.json())
#
#
# if __name__ == "__main__":
#     unittest.main()

import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api.dogs.router import admin_router  # Replace with your FastAPI app's main entry point
from config import AUTH_TOKEN
class TestDogRoutes(unittest.TestCase):
    def setUp(self):
        # Create a test client instance
        self.client = TestClient(admin_router)

    @patch("src.middleware.auth.aws_auth_strategy.RoleChecker")
    @patch("src.api.dogs.service.DogController")
    def test_admin_create_dog(self, mock_dog_service, mock_role_checker):
        # Mock the RoleChecker and DogController
        mock_role_checker.return_value = MagicMock()
        mock_dog_service.create_dog.return_value = {
            "id": "123",
            "name": "Buddy",
            "breed": "Labrador",
            "age": 3
        }

        payload = {
            "name": "Buddy",
            "breed": "Labrador",
            "age": 3
        }

        response = self.client.post(
            "/admin/dogs",
            json=payload,
            headers={"Authorization": "Bearer AUTH_TOKEN"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Buddy")

    @patch("src.middleware.auth.aws_auth_strategy.RoleChecker")
    @patch("src.api.dogs.service.DogController")
    def test_admin_get_dog(self, mock_dog_service, mock_role_checker):
        mock_role_checker.return_value = MagicMock()
        mock_dog_service.show_dog.return_value = {
            "id": "123",
            "name": "Buddy",
            "breed": "Labrador",
            "age": 3
        }

        response = self.client.get(
            "/admin/dogs/123",
            headers={"Authorization": "Bearer test_admin_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Buddy")

    @patch("src.middleware.auth.aws_auth_strategy.RoleChecker")
    @patch("src.api.dogs.service.DogController")
    def test_user_create_dog(self, mock_dog_service, mock_role_checker):
        mock_role_checker.return_value = MagicMock()
        mock_dog_service.create_dog.return_value = {
            "id": "456",
            "name": "Max",
            "breed": "Golden Retriever",
            "age": 2
        }

        payload = {
            "name": "Max",
            "breed": "Golden Retriever",
            "age": 2
        }

        response = self.client.post(
            "/user/dogs",
            json=payload,
            headers={"Authorization": "Bearer test_user_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Max")

    @patch("src.middleware.auth.aws_auth_strategy.RoleChecker")
    @patch("src.api.dogs.service.DogController")
    def test_user_get_dog(self, mock_dog_service, mock_role_checker):
        mock_role_checker.return_value = MagicMock()
        mock_dog_service.show_dog.return_value = {
            "id": "456",
            "name": "Max",
            "breed": "Golden Retriever",
            "age": 2
        }

        response = self.client.get(
            "/user/dogs/456",
            headers={"Authorization": "Bearer test_user_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Max")

    @patch("src.middleware.auth.aws_auth_strategy.RoleChecker")
    @patch("src.api.dogs.service.DogController")
    def test_user_list_dogs(self, mock_dog_service, mock_role_checker):
        mock_role_checker.return_value = MagicMock()
        mock_dog_service.list_dogs.return_value = {
            "dogs": [
                {"id": "123", "name": "Buddy", "breed": "Labrador", "age": 3},
                {"id": "456", "name": "Max", "breed": "Golden Retriever", "age": 2}
            ]
        }

        response = self.client.get(
            "/user/dogs",
            headers={"Authorization": "Bearer test_user_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dogs"]), 2)

if __name__ == "__main__":
    unittest.main()
