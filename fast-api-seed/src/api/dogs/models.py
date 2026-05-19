from datetime import datetime, timezone
from typing import Optional,Annotated
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from src.api.dogs.dog_enums import DogBreed,GenderEnum

# Annotate ObjectId for use with Pydantic models
PyObjectId = Annotated[str, BeforeValidator(str)]

# Pydantic model for a Dog with detailed attributes (for database storage)
class Dog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    breed:DogBreed
    age: int
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
                "gender": 1,
                "color": "white",
                "owner": "johndoe"

            }
        }

