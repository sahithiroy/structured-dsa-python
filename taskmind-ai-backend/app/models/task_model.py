from pydantic import BaseModel,Field,BeforeValidator
from bson import ObjectId
from typing import Optional,Annotated
from app.enums.task_enums import TaskStatus, TaskPriority

PyObjectId = Annotated[str, BeforeValidator(str)]

class Task(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus


