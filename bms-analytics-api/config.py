import os
from dotenv import load_dotenv

# Load environment variables from a .env file
# This allows sensitive configuration data (e.g., secrets, tokens, URLs) to be stored in a separate file
# and accessed securely in the application.
load_dotenv()

#
# Custom JWT configs
#

# The secret key used for encoding and decoding JWTs (JSON Web Tokens).
# This value should be securely stored and must not be shared publicly.
SECRET_KEY = os.getenv("SECRET_KEY")

# Retrieve the algorithm used for JWT token encoding/decoding.
# Common algorithms include HS256, RS256, etc. Ensure the algorithm matches the one used during token generation.
ALGORITHM = os.getenv("ALGORITHM")

# Retrieve the token expiration time in minutes.
# If the environment variable is not set, the default value is 30 minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

#
# Datastores
#

# The connection string for the MongoDB database.
# This typically includes information like the host, port, username, password, and database name.
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

#
# AWS Configs
#

# The default AWS region where resources (e.g., S3 buckets, Lambda functions) are hosted.
# Example: "us-east-1" or "eu-west-2".
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "")

# The secret access key for authenticating AWS SDK requests.
# This value should be stored securely and not hardcoded into the application code.
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

# The AWS account ID associated with the credentials.
# This can be used for resource identification in multi-account setups.
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", "")

# The access key ID for authenticating AWS SDK requests.
# Like the secret access key, this should be securely stored.
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")

# The environment in which the server is running (e.g., "development", "staging", "production").
# This can be used to adjust configurations or behaviors specific to the environment.
SERVER_ENV = os.getenv("SERVER_ENV", "")

ALERT_BASE_URL = os.getenv("ALERT_BASE_URL", "")
