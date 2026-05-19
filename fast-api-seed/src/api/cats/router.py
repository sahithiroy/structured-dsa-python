from typing import Optional
from fastapi import APIRouter, status, Request
from src.api.cats.models import Cat
from src.api.cats.payload import CreateCatDto, UpdateCatDto
from src.api.cats.service import CatService
from src.middleware.auth.cognito_user import CognitoUser
from src.middleware.auth.groups_required_decorator import groups_required
from src.middleware.auth.user_groups_enum import UserGroups

# Create a FastAPI router instance to define API endpoints
router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Cat)
@groups_required([UserGroups.AccountAdmin])  # Restrict access to AccountAdmin group
async def create_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Create a new cat.

    :param request: FastAPI request object to extract JSON payload.
    :param current_user: The currently authenticated user (CognitoUser).
    :return: The created Cat object.
    """
    # Extract the JSON payload from the request and validate it using CreateCatDto
    payload = await request.json()
    cat = CreateCatDto(**payload)
    # Initialize the service layer and delegate the creation logic
    cat_service = CatService()
    return await cat_service.create_cat(cat=cat, owner_id=current_user.sub)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[Cat])
@groups_required(
    [UserGroups.AccountAdmin, UserGroups.AccountUser])  # Allow access to AccountAdmin and AccountUser groups
async def get_cats(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Retrieve all cats owned by the authenticated user.

    :param request: FastAPI request object.
    :param current_user: The currently authenticated user (CognitoUser).
    :return: A list of Cat objects.
    """
    # Initialize the service layer and fetch the list of cats for the user
    cat_service = CatService()
    return await cat_service.list_cats(owner_id=current_user.sub)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Cat)
@groups_required(
    [UserGroups.AccountAdmin, UserGroups.AccountUser])  # Allow access to AccountAdmin and AccountUser groups
async def get_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Retrieve a specific cat by its ID and the current user's ownership.

    :param request: FastAPI request object.
    :param current_user: The currently authenticated user (CognitoUser).
    :return: The Cat object if found.
    """
    # Extract the cat ID from the request path parameters
    id: str = request.path_params.get("id", "")
    # Initialize the service layer and fetch the specific cat
    cat_service = CatService()
    return await cat_service.show_cat(id=id, owner_id=current_user.sub)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Cat)
@groups_required([UserGroups.AccountAdmin])  # Restrict access to AccountAdmin group
async def updates_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Update a cat's details.

    :param request: FastAPI request object to extract JSON payload.
    :param current_user: The currently authenticated user (CognitoUser).
    :return: The updated Cat object.
    """
    # Extract the cat ID from the request path parameters
    id: str = request.path_params.get("id", "")
    # Extract the JSON payload from the request and validate it using UpdateCatDto
    payload = await request.json()
    cat = UpdateCatDto(**payload)
    # Initialize the service layer and update the cat's details
    cat_service = CatService()
    return await cat_service.update_cat(id=id, owner_id=current_user.sub, cat=cat)


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Cat)
@groups_required([UserGroups.AccountAdmin])  # Restrict access to AccountAdmin group
async def deletes_cat(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Delete a specific cat by its ID and the current user's ownership.

    :param request: FastAPI request object.
    :param current_user: The currently authenticated user (CognitoUser).
    :return: The deleted Cat object.
    """
    # Extract the cat ID from the request path parameters
    id: str = request.path_params.get("id", "")
    # Initialize the service layer and delete the specified cat
    cat_service = CatService()
    cat = await cat_service.delete_cat(id=id, owner_id=current_user.sub)
    return cat
