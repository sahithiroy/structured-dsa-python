from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService


class AuthenticationRoute:

    def __init__(self, app):

        # Store FastAPI app
        self.app = app

        # Create router
        self.router = APIRouter(
            prefix="/auth",
            tags=["Authentication"]
        )

        # Initialize Auth Service
        self.auth_service = AuthService()

        # Register all routes
        self.register_routes()

        # Include router in app
        self.app.include_router(self.router)

    def register_routes(self):

        # Home Route
        @self.router.get("/")
        def home():
            return {
                "message": "Authentication Route Working"
            }

        # Register User Route
        @self.router.post("/register")
        def register_user(username: str, password: str):

            result = self.auth_service.register_user(
                username,
                password
            )

            if (
                "message" in result and
                result["message"] == "User already exists"
            ):
                raise HTTPException(
                    status_code=400,
                    detail=result["message"]
                )

            return result

        # Login User Route
        @self.router.post("/login")
        def login_user(username: str, password: str):

            result = self.auth_service.login_user(
                username,
                password
            )

            if (
                "message" in result and
                result["message"] == "Invalid username or password"
            ):
                raise HTTPException(
                    status_code=400,
                    detail=result["message"]
                )

            return result