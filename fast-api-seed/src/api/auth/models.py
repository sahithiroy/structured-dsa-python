from pydantic import BaseModel, Field
from typing import Optional


# Model representing a user with optional fields and default values
class User(BaseModel):
    username: str
    disabled: Optional[bool] = False
    role: str
    password: Optional[str] = Field(None, alias='password')
