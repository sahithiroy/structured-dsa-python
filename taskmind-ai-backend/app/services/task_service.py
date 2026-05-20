from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.database.mongodb import MongoDB
from app.models.task_model import Task
from bson import ObjectId
class TaskService:
    def __init__(self):
        self.db = MongoDB()

    async def init_db(self):
        await self.db.connectMongoDB()
        await self.db.create_database("Tasks")
        await self.db.create_collection("Task_data")
    async def create_task(self, task: TaskCreate):

        task_dict = task.dict()

        task_dict["priority"] = task.priority.value
        task_dict["status"] = task.status.value

        result = await self.db.insert_one(task_dict)

        return {
            "inserted_id": str(result.inserted_id),
            "message": "Task created successfully"
        }
    async def get_task(self,task_id)-> Task:
        print(f"Getting task with ID: {task_id}")
        task=await self.db.collection.find_one({"_id":ObjectId(task_id)})
        if task:
            return Task(**task)
        else:
            return {"message":"Task not found"}
    async def update_task(self, task_id, task: TaskUpdate):

        task_dict = task.model_dump(
            exclude_unset=True,
            mode="json"
        )

        result = await self.db.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": task_dict}
        )

        if result.modified_count:
            return {"message": "Task updated successfully"}

        return {"message": "Task not found or no changes made"}
    async def delete_task(self,task_id):
        print(f"Deleting task with ID: {task_id}")
        result= await self.db.collection.delete_one({"_id":ObjectId(task_id)})
        if result.deleted_count:
            return {"message":"Task deleted successfully"}
        else:
            return {"message":"Task not found"}
    async def list_tasks(self):
        tasks= await self.db.collection.find().to_list(length=None)
        task_list=[{"_id":str(task["_id"]),"title":task["title"],"description":task["description"]} for task in tasks]
        return {"tasks":task_list}
    