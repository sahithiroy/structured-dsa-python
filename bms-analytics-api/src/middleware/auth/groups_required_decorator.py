from functools import wraps
from typing import List
from fastapi import HTTPException, status

from src.middleware.auth.aws_auth_strategy import AWSAuthStrategy, oauth2_scheme
from src.middleware.auth.cognito_user import CognitoUser


async def get_current_user():
    """
    Mock function to retrieve the current user.
    """
    return {"username": "bhavya", "roles": ["AccountAdmin"]}


# Role-Based Access Control (RBAC) Decorator
def groups_required(roles: List[str]):
    """
    Decorator to enforce RBAC for FastAPI endpoints based on user roles.

    Args:
        roles (List[str]): A list of roles/groups required to access the endpoint.

    Returns:
        Function: The wrapped function with role-based access control applied.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract the request object from kwargs
            request = kwargs["request"]

            # Extract the token using the OAuth2 scheme.
            token = await oauth2_scheme(request)

            # Remove "Bearer " prefix from the token if it exists.
            token = str(token).replace("Bearer ", "")

            # Validate the token and retrieve user details from AWS Cognito.
            user = await AWSAuthStrategy().validate_token(token=token)

            # Populate the current_user object with Cognito user details.
            kwargs['current_user'] = CognitoUser(**user)

            # If no user is retrieved from the token, raise an unauthorized exception.
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid login. No user details found for token"
                )

            # Check if the user's groups contain any of the required roles.
            if not any(item in user.get("cognito:groups", []) for item in roles):
                # If no match is found, raise a forbidden access exception.
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access Denied. User does not have sufficient permissions to perform this action"
                )

            # Call the original function if validation passes.
            return await func(*args, **kwargs)

        return wrapper

    return decorator

