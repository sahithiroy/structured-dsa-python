from pydantic import BaseModel
from typing import List, Optional


class CognitoUser(BaseModel):
    sub: Optional[str] = None  # Unique user ID in Cognito
    username: Optional[str] = None  # Cognito username
    email: Optional[str] = None  # User email
    email_verified: Optional[bool] = None  # Email verification status
    phone_number: Optional[str] = None  # Optional phone number
    phone_number_verified: Optional[bool] = False  # Phone verification status
    cognito_groups: Optional[List[str]] = []  # Groups user belongs to
    given_name: Optional[str] = None  # First name
    family_name: Optional[str] = None  # Last name
    preferred_username: Optional[str] = None  # Preferred username
    custom_attributes: Optional[dict] = {}  # Custom Cognito attributes
