from functools import wraps
from typing import List

from fastapi import HTTPException, status

from src.middleware.auth.aws_auth_strategy import AWSAuthStrategy, oauth2_scheme
from src.middleware.auth.cognito_user import CognitoUser


async def get_current_user():
    # Logic to retrieve the user (e.g., from token or session)
    return {"username": "bhavya", "roles": ["AccountAdmin"]}


# RBAC Decorator
def groups_required(roles: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs["request"]
            token = await oauth2_scheme(request)
            token = str(token).replace("Bearer ", "")
            user = await AWSAuthStrategy().validate_token(token=token)
            kwargs['current_user'] = CognitoUser(**user)
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid login. No user details found for token")
            if not any(item in user.get("cognito:groups", []) for item in roles):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Access Denied. User does not have sufficient permissions to perform this action")
            return await func(*args, **kwargs)

        return wrapper

    return decorator
