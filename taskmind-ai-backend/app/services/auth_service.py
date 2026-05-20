from app.database.mongodb import MongoDB
from app.core.security import Security
from app.schemas.userSchema import UserLogin, User


class AuthService:

    def __init__(self):

        self.db = MongoDB()

        self.s = Security()

    async def init_db(self):

        await self.db.connectMongoDB()

        await self.db.create_database("Users")

        await self.db.create_collection("User_data")

    async def register_user(self, user: User) -> dict:

        existing_user = await self.db.collection.find_one(
            {"username": user.username}
        )

        if existing_user:

            return {"message": "User already exists"}

        hashed_password = self.s.get_password_hash(
            user.password
        )

        await self.db.insert_one({
            "username": user.username,
            "password": hashed_password,
            "role": user.role.value
        })

        return {"message": "User registered successfully"}

    async def login_user(self, user: UserLogin) -> dict:

        db_user = await self.db.collection.find_one(
            {"username": user.username}
        )

        if (
            db_user and
            self.s.verify_password(
                user.password,
                db_user["password"]
            )
        ):

            access_token = self.s.create_access_token(
                data={"sub": user.username,
                      "role": db_user["role"]}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }

        return {
            "message": "Invalid username or password"
        }