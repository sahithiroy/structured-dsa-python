from app.enums.task_enums import UserRole
from app.services.task_service import TaskService
from app.schemas.task_schema import TaskCreate, TaskUpdate
from fastapi import APIRouter, HTTPException
from app.models.task_model import Task
from fastapi import Depends
from app.middleware.auth_middleware import verify_token
from app.middleware.role_middleware import role_required

# Define the roles that are allowed to perform certain actions
ALLOWED_ROLES = [UserRole.ADMIN.value, UserRole.USER.value]

class TaskRoute:
    def __init__(self, app):
        self.app = app
        self.router = APIRouter(
            prefix="/tasks",
            tags=["Tasks"]
        )
        self.task_service = TaskService()
        self.register_routes()
        self.app.include_router(self.router)    
    def register_routes(self):
        @self.router.post("/create")
        async def create_task(task: TaskCreate, payload: dict = Depends(verify_token),user=Depends(role_required(ALLOWED_ROLES))):
            result = await self.task_service.create_task(task)
            return result
        @self.router.get("/{task_id}")
        async def get_task(task_id: str, payload: dict = Depends(verify_token),user=Depends(role_required(ALLOWED_ROLES)))-> Task:
            result = await self.task_service.get_task(task_id)
            if "message" in result and result["message"] == "Task not found":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        @self.router.put("/{task_id}")
        async def update_task(task_id: str, task: TaskUpdate, payload: dict = Depends(verify_token),user=Depends(role_required([UserRole.ADMIN.value]))):
            result = await self.task_service.update_task(task_id, task)
            if "message" in result and result["message"] == "Task not found or no changes made":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        @self.router.delete("/{task_id}")
        async def delete_task(task_id: str, payload: dict = Depends(verify_token),user=Depends(role_required([UserRole.ADMIN.value]))):
            result =  await self.task_service.delete_task(task_id)
            if "message" in result and result["message"] == "Task not found":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        @self.router.get("/")
        async def list_tasks(payload: dict = Depends(verify_token),user=Depends(role_required(ALLOWED_ROLES))):
            result =  await self.task_service.list_tasks()
            return result
        
