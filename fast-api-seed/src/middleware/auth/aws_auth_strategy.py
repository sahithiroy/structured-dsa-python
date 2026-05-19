import asyncio

import cognitojwt
import requests
from starlette.responses import JSONResponse

from config import AWS_DEFAULT_REGION
from src.middleware.auth.auth_service import get_user_pool_and_client_id, AuthService
from src.middleware.error.exceptions import ForbiddenAccessException, SessionExpiredException, PyJWTException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from jose import jwt, JWTError

# Define the OAuth2 password bearer scheme with the token URL.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# This function extracts the token from the request and validates it using the validate_token function.
# todo deprecated remove this
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Fetches the current user from token
    :param token: The token received in request
    :return:
    """
    return await validate_token(token)


class AWSAuthStrategy:
    async def validate_token(self, token: str):
        try:
            unverified_claims: dict = jwt.get_unverified_claims(token)
            tenant_namespace = unverified_claims['custom:companyNS']
            # Retrieve the user pool ID and client ID using the username
            auth_service = AuthService()
            stack_name = auth_service.generate_tenant_stack_name(tenant_namespace=tenant_namespace)
            user_pool_id, client_id = await auth_service.get_cognito_details_based_on_user_stack(
                stack_name=stack_name,
                is_super_admin=False
            )
            # Fetch the JWKS from the Cognito User Pool endpoint
            jwks_url = f"https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
            jwks_response = requests.get(jwks_url)
            jwks_response.raise_for_status()  # Raise an exception for bad status codes
            jwks = jwks_response.json()

            # Find the matching key ID (kid) from the JWT header
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')

            # Find the corresponding public key from the JWKS
            key = None
            for key_dict in jwks['keys']:
                if key_dict['kid'] == kid:
                    key = key_dict
                    break

            if key is None:
                raise SessionExpiredException(message=f"Public key not found in JWKS.")

            # Decode and verify the JWT
            decoded_payload = jwt.decode(
                token,
                key=key,
                algorithms=['RS256'],  # Adjust algorithm as needed
                audience=client_id,
                issuer=f'https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{user_pool_id}'
            )
            # return decoded_payload
            return decoded_payload

        except cognitojwt.CognitoJWTException as ce:
            raise SessionExpiredException(message=str(ce), err=ce)
        except JWTError as ce:
            raise PyJWTException(message=str(ce), err=ce)
        except Exception as e:
            raise PyJWTException(message=str(e), err=e)


async def validate_token(token: str):
    try:
        # Extract headers from the token without verifying its signature
        headers = jwt.get_unverified_header(token)
        kid = headers.get('kid')  # Get the 'kid' (key ID) from the headers
        if not kid:
            raise SessionExpiredException("Invalid token")

        # Extract the username from the token claims without verifying its signature
        username = jwt.get_unverified_claims(token).get('username')
        print('validatetoken')
        print('username',username)
        if not username:
            raise SessionExpiredException("Invalid token")

        # Retrieve the user pool ID and client ID using the username
        user_pool_id, client_id = get_user_pool_and_client_id(username)

        # # Construct the URL to fetch the JWKS (JSON Web Key Set) from Cognito
        # cognito_keys_url = f"https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

        loop = asyncio.get_event_loop()
        print("loop",loop)
        payload = await loop.run_in_executor(
            None,
            cognitojwt.decode,
            token,
            AWS_DEFAULT_REGION,
            user_pool_id,
            client_id
        )
        print('payload',payload)
        return payload
    except cognitojwt.CognitoJWTException as e:
        # Handle JWT-related errors and raise an HTTPException with details
        print(e)
        return JSONResponse(
            status_code=401,
            content={
                "statusCode": 401,
                "errorCode": "INVALID_TOKEN",
                "message": "Token Validation failed",
                "description": "Token Validation failed",
                "detail": f"Token validation failed: {str(e)}"
            },
        )


# todo deprecated => remove it later
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: dict = Depends(get_current_user)):
        role = current_user.get("role")  # Single role as a string
        print('Role:', role)
        print("allowed_roles", self.allowed_roles)
        if role not in self.allowed_roles:  # Direct string comparison
            raise ForbiddenAccessException
        return current_user
