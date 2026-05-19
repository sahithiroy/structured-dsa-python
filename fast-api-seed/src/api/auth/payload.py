from pydantic import BaseModel, Field
from typing import Optional, List
from src.api.common_enums import Role


# Model representing an access token
class Token(BaseModel):
    access_token: str  # The JWT access token string
    token_type: str  # Type of token, e.g., "bearer"


# Model representing token data, typically used to extract user information from the token
class TokenData(BaseModel):
    username: Optional[str] = None  # Optional username extracted from the token


# Base model representing a user with username and role
class User(BaseModel):
    username: str
    cognito_groups: List[str] = Field(..., alias="cognito:groups")

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "roles": ["AccountAdmin"]
            }
        }


# Extended model for users stored in the database, including hashed password
class UserInDB(User):
    hashed_password: str
