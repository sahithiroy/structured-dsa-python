import json

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from requests import Request
from starlette import status
from starlette.responses import Response

from src.middleware.error.exceptions import CustomHTTPException


def _generate_code_from_status(http_status: int):
    """
    Generate a custom error code based on HTTP status.

    Args:
        http_status (int): The HTTP status code.

    Returns:
        str: A custom error code corresponding to the HTTP status.
    """
    if http_status == status.HTTP_401_UNAUTHORIZED:
        return "NOT_AUTHENTICATED"
    if http_status == status.HTTP_403_FORBIDDEN:
        return "ACCESS_DENIED"
    if http_status == status.HTTP_400_FORBIDDEN:
        return "BAD_REQUEST"
    else:
        return "GENERAL_ERROR"


# Custom exception handler for standard HTTP exceptions
def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """
    Handle HTTP exceptions raised in the application.

    Args:
        request (Request): The incoming HTTP request.
        exc (HTTPException): The raised HTTP exception.

    Returns:
        Response: A JSON response with error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "errorCode": _generate_code_from_status(exc.status_code),
            "message": exc.detail,
            "description": exc.detail,
            "details": str(exc),
        },
    )


# Custom exception handler for `CustomHTTPException`
def custom_http_exception_handler(request: Request, exc: CustomHTTPException) -> Response:
    """
    Handle custom HTTP exceptions specific to the application.

    Args:
        request (Request): The incoming HTTP request.
        exc (CustomHTTPException): The raised custom HTTP exception.

    Returns:
        Response: A JSON response with error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "errorCode": exc.error_code,
            "message": exc.message,
            "description": exc.description,
            "details": exc.details,
        },
    )


# General exception handler for unexpected errors
def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions that occur in the application.

    Args:
        request (Request): The incoming HTTP request.
        exc (Exception): The raised general exception.

    Returns:
        Response: A JSON response indicating an internal server error.
    """
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "errorCode": "GENERAL_ERROR",
            "message": str(exc),
            "description": "An unexpected error occurred",
            "detail": str(exc)
        }
    )


# Custom validation exception handler for FastAPI payload validation
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle payload validation errors raised by FastAPI.

    Args:
        request (Request): The incoming HTTP request.
        exc (RequestValidationError): The raised validation error.

    Returns:
        Response: A JSON response with validation error details.
    """
    errors = exc.errors()
    details = []
    for error in errors:
        location = error['loc'][1:]  # Remove 'body' from the location
        details.append({
            "key": location[-1],  # The field that caused the error
            "value": error['ctx']['input'] if 'ctx' in error else None,
            "error": [error['msg']]  # The error message
        })

    return JSONResponse(
        status_code=400,
        content={
            "statusCode": 400,
            "errorCode": "INVALID_PAYLOAD",
            "message": "Invalid payload received",
            "description": "Invalid payload received",
            "details": [details]
        }
    )


# Custom validation exception handler for Pydantic validation errors
def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """
    Handle Pydantic validation errors raised during data validation.

    Args:
        request (Request): The incoming HTTP request.
        exc (ValidationError): The raised Pydantic validation error.

    Returns:
        Response: A JSON response with validation error details.
    """
    print(exc.json())  # Log the validation error for debugging
    errors: dict = json.loads(exc.json())  # Parse the validation error details
    messages = list(
        map(lambda error: f"'{error.get('loc', [])[0]}' {error.get('msg', '').replace('Input ', '')}", errors))

    return JSONResponse(
        status_code=400,
        content={
            "statusCode": 400,
            "errorCode": "INVALID_PAYLOAD",
            "message": "Invalid payload received",
            "description": messages,  # Summarized error messages
            "details": errors  # Full error details
        }
    )
