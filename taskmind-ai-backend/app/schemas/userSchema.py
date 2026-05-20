from pydantic import BaseModel
from app.enums.task_enums import UserRole
class User(BaseModel):
    username: str
   
    password: str
    role: UserRole
class UserLogin(BaseModel):
    username: str
    password: str
