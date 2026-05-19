from app.services.task_service import TaskService
from app.schemas.task_schema import TaskCreate, TaskUpdate
from fastapi import APIRouter, HTTPException
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
        @self.router.post("/")
        def create_task(task: TaskCreate):
            result = self.task_service.create_task(task)
            return result
        @self.router.get("/{task_id}")
        def get_task(task_id: str):
            result = self.task_service.get_task(task_id)
            if "message" in result and result["message"] == "Task not found":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        @self.router.put("/{task_id}")
        def update_task(task_id: str, task: TaskUpdate):
            result = self.task_service.update_task(task_id, task)
            if "message" in result and result["message"] == "Task not found or no changes made":
                raise HTTPException(status_code=404, detail=result["message"])
            return result
        @self.router.delete("/{task_id}")
        def delete_task(task_id: str):
            result = self.task_service.delete_task(task_id)
            if "message" in result and result["message"] == "Task not found":
                raise HTTPException(status_code=404, detail=result["message"])
            return result