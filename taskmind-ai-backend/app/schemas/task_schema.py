from typing import Optional

from pydantic import BaseModel
from app.enums.task_enums import TaskStatus, TaskPriority
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
