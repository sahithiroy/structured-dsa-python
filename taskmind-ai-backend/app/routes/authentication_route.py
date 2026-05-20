from fastapi import APIRouter, HTTPException

from app.services.auth_service import AuthService

from app.schemas.userSchema import User, UserLogin


class AuthenticationRoute:

    def __init__(self, app):

        self.app = app

        self.router = APIRouter(
            prefix="/auth",
            tags=["Authentication"]
        )

        self.auth_service = AuthService()

        self.register_routes()

        self.app.include_router(self.router)

    def register_routes(self):

        @self.router.get("/")
        def home():

            return {
                "message": "Authentication Route Working"
            }

        # REGISTER
        @self.router.post("/register")
        async def register_user(user: User):

            result = await self.auth_service.register_user(
                user
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

        # LOGIN
        @self.router.post("/login")
        async def login_user(user: UserLogin):

            result = await self.auth_service.login_user(
                user
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