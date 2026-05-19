from fastapi import HTTPException
from typing import Dict, Any, Optional


# Base class for custom HTTP exceptions with extended error information
class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, error_code: str,
                 additional_details: Optional[Dict[str, Any]] = None, err: Optional[Exception] = None):
        # Construct the error response
        error = {
            "statusCode": status_code,
            "errorCode": error_code,
            "message": message,
            "description": str(err) if err else message,
        }
        if additional_details:
            error["details"] = [additional_details]  # Add additional details if provided
        super().__init__(status_code=status_code, detail=error)  # Initialize the base HTTPException
        self.error_code = error_code  # Custom error code
        self.message = message
        self.error_code = error_code
        self.description = str(err) if err else message  # Description of the error
        self.details = additional_details  # Additional details about the error
        self.error_details = str(err) if err else ""  # Detailed error message if an exception is provided

    # Create a CustomHTTPException instance from a JSON dictionary
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "CustomHTTPException":
        return cls(
            status_code=data.get("statusCode", 500),
            message=data.get("message", "Error Occurred"),
            error_code=data.get("errorCode", "GENERAL_ERROR"),
            additional_details=data.get("details", None)
        )

    # Getters for error information
    def get_error_code(self) -> str:
        return self.error_code

    def get_details(self) -> Optional[Dict[str, Any]]:
        return self.details

    def get_description(self) -> str:
        return self.description

    def get_error_details(self) -> str:
        return self.error_details


# Exception for resource not found errors
class ResourceNotFoundException(CustomHTTPException):
    def __init__(self, message: str, id: str, err: Optional[Exception] = None):
        super().__init__(status_code=404, message=message, error_code="RESOURCE_NOT_FOUND",
                         additional_details={"id": id}, err=err)


# Exception for session expiration errors
class SessionExpiredException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        super().__init__(status_code=401, message=message, error_code="SESSION_EXPIRED", err=err)


# Exception for unauthorized access errors
class UnauthorizedAccessException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        super().__init__(status_code=401, message=message, error_code="UNAUTHORIZED_ACCESS", err=err)


# Exception for forbidden access errors
class ForbiddenAccessException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        super().__init__(status_code=403, message=message, error_code="FORBIDDEN_ACCESS", err=err)


# Exception for invalid token signature errors
class InvalidSignatureException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        super().__init__(status_code=401, message=message, error_code="INVALID_SIGNATURE", err=err)


# Exception for JWT token errors (e.g., token expired)
class PyJWTException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        super().__init__(status_code=401, message=message, error_code="JWT_FAILURE", err=err)
