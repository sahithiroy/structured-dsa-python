import json

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from requests import Request
from starlette import status
from starlette.responses import Response

from src.middleware.error.exceptions import CustomHTTPException


def _generate_code_from_status(http_status: int):
    if http_status == status.HTTP_401_UNAUTHORIZED:
        return "NOT_AUTHENTICATED"
    if http_status == status.HTTP_403_FORBIDDEN:
        return "ACCESS_DENIED"
    if http_status == status.HTTP_400_FORBIDDEN:
        return "BAD_REQUEST"
    else:
        return "GENERAL_ERROR"


# Custom exception handler
def http_exception_handler(request: Request, exc: HTTPException) -> Response:
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


# Custom exception handler
def custom_http_exception_handler(request: Request, exc: CustomHTTPException) -> Response:
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


# General exception handler
def general_exception_handler(request: Request, exc: Exception):
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


# Custom Payload validation handler
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    details = []
    for error in errors:
        location = error['loc'][1:]  # Remove 'body'
        details.append({
            "key": location[-1],  # Take the last element of the location array
            "value": error['ctx']['input'] if 'ctx' in error else None,
            "error": [error['msg']]
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


# Custom Payload validation handler
def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    print(exc.json())
    errors: dict = json.loads(exc.json())
    messages = list(
        map(lambda error: f"'{error.get('loc', [])[0]}' {error.get('msg', '').replace('Input ', '')}", errors))

    return JSONResponse(
        status_code=400,
        content={
            "statusCode": 400,
            "errorCode": "INVALID_PAYLOAD",
            "message": "Invalid payload received",
            "description": messages,
            "details": errors
        }
    )
