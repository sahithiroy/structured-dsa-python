from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.database.mongodb import MongoDB
class TaskService:
    def __init__(self):
        self.db=MongoDB()
        self.db.connectMongoDB()
        self.db.create_database("Tasks")
        self.db.create_collection("Task_data")
    def create_task(self,task: TaskCreate)-> dict:
        task_dict=task.dict()
        result=self.db.insert_one(task_dict)
        return {"message":"Task created successfully","task_id":str(result.inserted_id)}
    def get_task(self,task_id)-> dict:
        task=self.db.collection.find_one({"_id":task_id})
        if task:
            task["_id"]=str(task["_id"])
            return task
        else:
            return {"message":"Task not found"}
    def update_task(self,task_id,task: TaskUpdate)-> dict:
        task_dict=task.dict(exclude_unset=True)
        result=self.db.collection.update_one({"_id":task_id},{"$set":task_dict})
        if result.modified_count:
            return {"message":"Task updated successfully"}  
        else:
            return {"message":"Task not found or no changes made"}
    def delete_task(self,task_id)-> dict:
        result=self.db.collection.delete_one({"_id":task_id})
        if result.deleted_count:
            return {"message":"Task deleted successfully"}
        else:
            return {"message":"Task not found"}
    def list_tasks(self)-> dict:
        tasks=self.db.collection.find()
        task_list=[{"_id":str(task["_id"]),"title":task["title"],"description":task["description"]} for task in tasks]
        return {"tasks":task_list}
    