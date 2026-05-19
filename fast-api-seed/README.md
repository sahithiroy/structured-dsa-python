# Zyrone Energy - FastAPI Application

Seed Application

# Installing Dependencies

```
pip install -r requirements.txt
```

# Supported ENV variables

```
MONGODB_URL=your-mongo-url
SECRET_KEY=secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

# Command to run the application 

```
uvicorn main:app --reload
```
After running the command open http://localhost:8000/docs
This is where we will test our code
![image](https://github.com/user-attachments/assets/67a85b20-7663-405c-8c77-8aa83e519c17)

First we need to authorize to access the routes to do that click on Authoriza which in top right above the operations

![image](https://github.com/user-attachments/assets/dce337b5-0d37-474a-9703-eb36bda97101)

Example: 

usernams: johndoe

password: secret
