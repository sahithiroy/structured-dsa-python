# This can be used to adjust configurations or behaviors specific to the environment.
import os

SERVER_ENV = os.getenv("SERVER_ENV", "dev")
SECRETS_NAME = os.getenv("SECRETS_NAME", "server-managed-secret-manager")
ALERT_BASE_URL = os.getenv("ALERT_BASE_URL", "https://dev.api.zyroneenergy.com")
