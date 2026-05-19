from src.middleware.error.exceptions import SessionExpiredException
from fastapi import APIRouter, HTTPException
from src.api.auth.models import User
from src.api.auth.utils import get_password_hash, get_user_by_username
from src.api.auth.database import users_collection

router = APIRouter()

# Route to register a new user
@router.post("/auth/register")
async def register_user(user: User):
    # Check if the user already exists
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = await get_password_hash(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    user_data["role"] = user.role  # Default role for new users

    # Insert new user into the database
    result = await users_collection.insert_one(user_data)
    if result.inserted_id:
        return {"message": "User registered successfully"}
    raise SessionExpiredException(status_code=500, detail="User registration failed")

# Route to login and generate an access token
# @router.post("/auth/token", response_model=Token)
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     try:
#         user = await authenticate_user(form_data.username, form_data.password)
#         # Authenticate user with provided credentials
#         if not user:
#             raise SessionExpiredException("Incorrect username or password.")
#
#         # Create an access token with expiration time
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#         return Token(access_token=access_token, token_type="bearer")
#     except Exception as e:
#         raise e
