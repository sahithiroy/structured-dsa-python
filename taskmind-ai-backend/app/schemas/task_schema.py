from pydantic import BaseModel
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    priority: str = None
    status: str = None
