from datetime import datetime, timezone
from pydantic import BaseModel, Field
from src.api.cats.cat_breed_enum import CatBreed


# Pydantic model for a Cat with detailed attributes (getting data)
class Cat(BaseModel):
    id: str
    name: str
    breed: CatBreed
    age: int
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
                "owner": "johndoe",
            }
        }
