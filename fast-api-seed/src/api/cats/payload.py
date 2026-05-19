from datetime import datetime, timezone
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

from src.api.cats.cat_breed_enum import CatBreed


# Pydantic model for a Cat with detailed attributes (getting data)
class CreateCatDto(BaseModel):
    name: str
    breed: CatBreed
    age: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Leo",
                "breed": "Siamese",
                "age": 1,
                "owner": "johndoe",
            }
        }


# Pydantic model for updating a Cat with optional fields
class UpdateCatDto(BaseModel):
    name: Optional[str] = None
    breed: Optional[CatBreed] = None
    age: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Leo",
                "breed": "Siamese",
                "age": 1
            }
        }
