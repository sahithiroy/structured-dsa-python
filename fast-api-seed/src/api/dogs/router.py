from fastapi import APIRouter
from typing import Optional
from src.api.dogs.models import Dog
from src.api.dogs.service import DogService
from src.api.dogs.payload import DogModelDTO, UpdateDogModel
from src.middleware.auth.cognito_user import CognitoUser
from src.middleware.auth.groups_required_decorator import groups_required
from src.middleware.auth.user_groups_enum import UserGroups
from fastapi import status, Request

# Create a FastAPI router to define routes for dog-related endpoints
router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=Dog)
@groups_required([UserGroups.AccountAdmin])  # Restrict access to AccountAdmin users
async def create_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Endpoint to create a new dog entry.

    :param request: The incoming HTTP request object.
    :param current_user: The currently authenticated Cognito user.
    :return: The created Dog object.
    """
    # Parse the JSON payload from the request
    payload = await request.json()
    # Create a DogModelDTO object from the payload
    dog = DogModelDTO(**payload)
    # Instantiate the DogService
    dog_service = DogService()
    # Call the service to create a dog and associate it with the current user
    return await dog_service.create_dog(dog=dog, owner_id=current_user.sub)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[Dog])
@groups_required([UserGroups.AccountAdmin, UserGroups.AccountUser])  # Allow access to both admins and users
async def get_cats(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Endpoint to list all dogs owned by the current user.

    :param request: The incoming HTTP request object.
    :param current_user: The currently authenticated Cognito user.
    :return: A list of Dog objects owned by the user.
    """
    # Instantiate the DogService
    dog_service = DogService()
    # Call the service to retrieve the list of dogs for the current user
    return await dog_service.list_dogs(owner_id=current_user.sub)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Dog)
@groups_required([UserGroups.AccountAdmin, UserGroups.AccountUser])  # Allow access to both admins and users
async def get_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Endpoint to retrieve details of a specific dog by its ID.

    :param request: The incoming HTTP request object.
    :param current_user: The currently authenticated Cognito user.
    :return: The Dog object if found.
    """
    # Extract the dog ID from the request path parameters
    id: str = request.path_params.get("id", "")
    # Instantiate the DogService
    dog_service = DogService()
    # Call the service to fetch the dog details for the given ID and owner
    return await dog_service.show_dog(id=id, owner_id=current_user.sub)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Dog)
@groups_required([UserGroups.AccountAdmin])  # Restrict access to AccountAdmin users
async def updates_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Endpoint to update details of a specific dog.

    :param request: The incoming HTTP request object.
    :param current_user: The currently authenticated Cognito user.
    :return: The updated Dog object.
    """
    # Extract the dog ID from the request path parameters
    id: str = request.path_params.get("id", "")
    # Parse the JSON payload from the request
    payload = await request.json()
    # Create an UpdateDogModel object from the payload
    dog = UpdateDogModel(**payload)
    # Instantiate the DogService
    dog_service = DogService()
    # Call the service to update the dog's details
    return await dog_service.update_dog(id=id, owner_id=current_user.sub, dog=dog)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Dog)
@groups_required([UserGroups.AccountAdmin])  # Restrict access to AccountAdmin users
async def deletes_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Endpoint to delete a specific dog by its ID.

    :param request: The incoming HTTP request object.
    :param current_user: The currently authenticated Cognito user.
    :return: The deleted Dog object.
    """
    # Extract the dog ID from the request path parameters
    id: str = request.path_params.get("id", "")
    # Instantiate the DogService
    dog_service = DogService()
    # Call the service to delete the dog and return the deleted object
    dog = await dog_service.delete_dog(id=id, owner_id=current_user.sub)
    return dog

