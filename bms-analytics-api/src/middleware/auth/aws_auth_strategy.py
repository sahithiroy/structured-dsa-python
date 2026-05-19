import cognitojwt
import requests
from config import AWS_DEFAULT_REGION
from src.middleware.auth.auth_service import  AuthService
from src.middleware.error.exceptions import  SessionExpiredException, PyJWTException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

# Define the OAuth2 password bearer scheme with the token URL.
# This helps in extracting the token from the "Authorization" header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AWSAuthStrategy:
    async def validate_token(self, token: str):
        """
        Validates the JWT token using AWS Cognito.

        Args:
            token (str): The JWT token to validate.

        Returns:
            dict: The decoded payload if the token is valid.

        Raises:
            SessionExpiredException: If the session is expired or invalid.
            PyJWTException: For errors during token decoding.
        """
        try:
            # Extract unverified claims from the token (without signature verification).
            unverified_claims: dict = jwt.get_unverified_claims(token)

            # Extract the custom tenant namespace from the claims.
            tenant_namespace = unverified_claims['custom:companyNS']

            # Initialize the AuthService to get user pool and client details.
            auth_service = AuthService()

            # Generate the stack name for the tenant using the namespace.
            stack_name = auth_service.generate_tenant_stack_name(tenant_namespace=tenant_namespace)

            # Fetch the Cognito User Pool ID and Client ID based on the tenant's stack.
            user_pool_id, client_id = await auth_service.get_cognito_details_based_on_user_stack(
                stack_name=stack_name,
                is_super_admin=False
            )

            # Construct the URL for the JWKS (JSON Web Key Set) for the Cognito User Pool.
            jwks_url = f"https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

            # Fetch the JWKS from the Cognito User Pool endpoint.
            jwks_response = requests.get(jwks_url)
            jwks_response.raise_for_status()  # Raise an exception for HTTP errors.
            jwks = jwks_response.json()

            # Extract the key ID (kid) from the JWT header.
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')

            # Find the public key in the JWKS that matches the "kid".
            key = None
            for key_dict in jwks['keys']:
                if key_dict['kid'] == kid:
                    key = key_dict
                    break

            # If no matching public key is found, raise an exception.
            if key is None:
                raise SessionExpiredException(message=f"Public key not found in JWKS.")

            # Decode and verify the JWT using the matching public key.
            decoded_payload = jwt.decode(
                token,
                key=key,  # The matching public key.
                algorithms=['RS256'],  # The algorithm used to sign the token.
                audience=client_id,  # The expected audience (client ID).
                issuer=f'https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{user_pool_id}'  # Expected issuer.
            )

            # Return the decoded payload if validation is successful.
            return decoded_payload

        except cognitojwt.CognitoJWTException as ce:
            # Handle exceptions specific to Cognito JWT validation.
            raise SessionExpiredException(message=str(ce), err=ce)
        except JWTError as ce:
            # Handle generic JWT errors.
            raise PyJWTException(message=str(ce), err=ce)
        except Exception as e:
            # Handle any other exceptions and wrap them in a PyJWTException.
            raise PyJWTException(message=str(e), err=e)





