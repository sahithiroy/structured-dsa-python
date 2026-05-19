import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

#
# Custom JWT configs
#
SECRET_KEY = os.getenv("SECRET_KEY")
# Retrieve the algorithm used for token encoding/decoding
ALGORITHM = os.getenv("ALGORITHM")
# Retrieve the token expiration time in minutes; default to 30 minutes if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

#
# Datastores
#
MONGODB_URL = os.getenv("MONGODB_URL")

#
# AWS Configs
#
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
SERVER_ENV = os.getenv("SERVER_ENV", "")

AUTH_TOKEN=os.getenv("AUTH_TOKEN","")
