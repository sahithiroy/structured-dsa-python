from app.routes.authentication_route import AuthenticationRoute
from app.routes.task_route import TaskRoute
from fastapi import FastAPI
app = FastAPI()
class Main:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        AuthenticationRoute(self.app)
        TaskRoute(self.app)
Main(app)