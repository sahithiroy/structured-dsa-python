from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()
URL = os.getenv("URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Security:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM  
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
    def verify_password(self, plain_password, hashed_password)-> bool:
        print("Verifying password...")
        return self.pwd_context.verify(plain_password, hashed_password)
    def get_password_hash(self, password)-> str:
        print("Hashing password...")
        return self.pwd_context.hash(password)
    def create_access_token(self, data: dict, expires_delta: timedelta = None)-> str:
        print("Creating access token...")
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
