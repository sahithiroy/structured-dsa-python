from datetime import datetime, timezone, timedelta

from src.api.auth.payload import TokenData, UserInDB
from src.middleware.error.exceptions import InvalidSignatureException, PyJWTException
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from jwt import JWT
import logging

from src.api.auth.models import User
from config import SECRET_KEY, ALGORITHM
from src.api.auth.database import users_collection

# Create a password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

jwt_instance = JWT()
# Retrieve a user by username from the database
async def get_user_by_username(username: str):
    user = await users_collection.find_one({"username": username})
    if user:
        return UserInDB(**user)
    return None

# Verify a provided password against a hashed password
async def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

# Hash a password for secure storage
async def get_password_hash(password: str):
    return pwd_context.hash(password)

# Authenticate a user by checking username and password
async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user

# Create an access token with optional expiration
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy() # Copy data to avoid modifying original

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta # Set expiration time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Default expiration time
    to_encode.update({"exp": expire})# Add expiration to payload
    encoded_jwt = jwt_instance.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Encode payload to JWT
    return encoded_jwt

# Retrieve and validate the current user from the token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = PyJWTException("Could not validate credentials")
    try:
        payload = jwt_instance.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decode JWT payload
        logging.info(f"Token payload: {payload}") # Log payload for debugging
        username: str = payload.get("sub") # Extract username from payload
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username) # Create TokenData object
        user = await get_user_by_username(token_data.username) # Fetch user from database
        if user is None:
            raise credentials_exception
        return user
    except jwt_instance.ExpiredSignatureError:
        raise InvalidSignatureException("Token has expired")
    except jwt_instance.InvalidTokenError:
        raise InvalidSignatureException("Invalid token")

# Retrieve the current active user, checking for inactive status
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Retrieve the current active admin user, checking for admin role
async def get_current_active_admin(current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.role != "admin":
        raise PyJWTException("Inactive user")
    return current_user


