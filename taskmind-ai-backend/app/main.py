from fastapi import FastAPI

from app.routes.task_route import TaskRoute
from app.routes.authentication_route import AuthenticationRoute

app = FastAPI()

task_route = TaskRoute(app)
auth_route = AuthenticationRoute(app)


@app.on_event("startup")
async def startup():

    await task_route.task_service.init_db()

    await auth_route.auth_service.init_db()