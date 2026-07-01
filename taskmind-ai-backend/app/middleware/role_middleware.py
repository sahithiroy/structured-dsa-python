from fastapi import Depends, HTTPException

from app.middleware.auth_middleware import verify_token


def role_required(required_roles: list):

    async def role_checker(
        user=Depends(verify_token)
    ):

        user_role = user.get("role")

        if user_role not in required_roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return role_checker

#RBAC decorator
def rbac(required_roles: list):

    def decorator(func):

        async def wrapper(*args, **kwargs):
            user = await role_required(required_roles)(*args, **kwargs)
            return await func(*args, **kwargs)

        return wrapper

    return decorator
