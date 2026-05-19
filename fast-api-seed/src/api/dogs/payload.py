from datetime import datetime, timezone
from typing import Optional, List, Annotated

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from src.api.dogs.dog_enums import DogBreed,GenderEnum
from src.api.dogs.models import Dog
# Annotate ObjectId for use with Pydantic models
PyObjectId = Annotated[str, BeforeValidator(str)]


# Pydantic model for a Dog with detailed attributes (Data Transfer Object - DTO)
class DogModelDTO(BaseModel):
    id:Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    breed: DogBreed
    age: Optional[int] = None
    gender:GenderEnum
    color: Optional[str] = None
    owner: str
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
                "gender":1,
                "color":"white",
                "owner": "johndoe"
            }
        }

#
#
# Pydantic model for updating a Dog with optional fields
class UpdateDogModel(BaseModel):
    name: Optional[str] = None
    breed: Optional[DogBreed] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    color: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Leo",
                "breed": "Siamese",
                "age": 1,
                "gender": "male",
                "color": "white",

            }
        }


# Pydantic model for a collection of dogs
class DogCollection(BaseModel):
    dogs: List[Dog]