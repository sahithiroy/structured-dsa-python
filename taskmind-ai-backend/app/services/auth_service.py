from app.database.mongodb import MongoDB
from app.models.user_models import User
from app.core.security import Security
from app.schemas.userSchema import UserLogin
class AuthService:
    def __init__(self):
        self.db=MongoDB()
        self.s=Security()
        self.db.connectMongoDB()
        self.db.create_database("Users")
        self.db.create_collection("User_data")
    def register_user(self,user: User)-> dict:
        user=self.db.collection.find_one({"username":user.username})
        if user:
            return {"message":"User already exists"}
        else:
            hashed_password=self.s.get_password_hash(user.password)
            self.db.insert_one({"username":user.username,"password":hashed_password})
            return {"message":"User registered successfully"}
    def login_user(self,user: UserLogin)-> dict:
        user=self.db.collection.find_one({"username":user.username})
        if user and self.s.verify_password(user.password,user["password"]):
            access_token=self.s.create_access_token(data={"sub":user.username})
            return {"access_token":access_token,"token_type":"bearer"}
        else:
            return {"message":"Invalid username or password"}

    