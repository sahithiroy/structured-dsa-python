from fastapi import HTTPException
from typing import Dict, Any, Optional


# Base class for custom HTTP exceptions with extended error information
class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, error_code: str,
                 additional_details: Optional[Dict[str, Any]] = None, err: Optional[Exception] = None):
        """
        Initialize a custom HTTP exception with additional error details.

        Parameters:
        - status_code: HTTP status code for the response (e.g., 404, 401).
        - message: Human-readable error message.
        - error_code: Custom error code for identifying the type of error.
        - additional_details: Additional context or details about the error (optional).
        - err: Optional exception object containing error details.
        """
        # Construct the error response payload
        error = {
            "statusCode": status_code,  # HTTP status code
            "errorCode": error_code,  # Custom error code
            "message": message,  # Human-readable error message
            "description": str(err) if err else message,  # Detailed description or fallback to message
        }
        # Add additional details if provided
        if additional_details:
            error["details"] = [additional_details]
        # Initialize the base HTTPException with the constructed error response
        super().__init__(status_code=status_code, detail=error)

        # Set instance attributes for easy access to error properties
        self.error_code = error_code
        self.message = message
        self.description = str(err) if err else message
        self.details = additional_details
        self.error_details = str(err) if err else ""

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "CustomHTTPException":
        """
        Create a `CustomHTTPException` instance from a JSON dictionary.

        Parameters:
        - data: A dictionary containing error details (e.g., statusCode, message, errorCode, details).

        Returns:
        - An instance of `CustomHTTPException`.
        """
        return cls(
            status_code=data.get("statusCode", 500),  # Default to 500 if statusCode is not provided
            message=data.get("message", "Error Occurred"),  # Default message if not provided
            error_code=data.get("errorCode", "GENERAL_ERROR"),  # Default error code if not provided
            additional_details=data.get("details", None)  # Additional details about the error
        )

    # Getters for error information
    def get_error_code(self) -> str:
        """Retrieve the custom error code."""
        return self.error_code

    def get_details(self) -> Optional[Dict[str, Any]]:
        """Retrieve the additional error details."""
        return self.details

    def get_description(self) -> str:
        """Retrieve the error description."""
        return self.description

    def get_error_details(self) -> str:
        """Retrieve the detailed error message if an exception was provided."""
        return self.error_details


# Exception for resource not found errors
class ResourceNotFoundException(CustomHTTPException):
    def __init__(self, message: str, id: str, err: Optional[Exception] = None):
        """
        Exception raised when a resource is not found.

        Parameters:
        - message: Error message.
        - id: Identifier of the missing resource.
        - err: Optional exception object.
        """
        super().__init__(status_code=404, message=message, error_code="RESOURCE_NOT_FOUND",
                         additional_details={"id": id}, err=err)


# Exception for session expiration errors
class SessionExpiredException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        """
        Exception raised when a user session has expired.

        Parameters:
        - message: Error message.
        - err: Optional exception object.
        """
        super().__init__(status_code=401, message=message, error_code="SESSION_EXPIRED", err=err)


# Exception for unauthorized access errors
class UnauthorizedAccessException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        """
        Exception raised for unauthorized access attempts.

        Parameters:
        - message: Error message.
        - err: Optional exception object.
        """
        super().__init__(status_code=401, message=message, error_code="UNAUTHORIZED_ACCESS", err=err)


# Exception for forbidden access errors
class ForbiddenAccessException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        """
        Exception raised when access to a resource is forbidden.

        Parameters:
        - message: Error message.
        - err: Optional exception object.
        """
        super().__init__(status_code=403, message=message, error_code="FORBIDDEN_ACCESS", err=err)


# Exception for invalid token signature errors
class InvalidSignatureException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        """
        Exception raised for invalid JWT token signatures.

        Parameters:
        - message: Error message.
        - err: Optional exception object.
        """
        super().__init__(status_code=401, message=message, error_code="INVALID_SIGNATURE", err=err)


# Exception for JWT token errors (e.g., token expired)
class PyJWTException(CustomHTTPException):
    def __init__(self, message: str, err: Optional[Exception] = None):
        """
        Exception raised for JWT token-related issues (e.g., expiration, decoding failure).

        Parameters:
        - message: Error message.
        - err: Optional exception object.
        """
        super().__init__(status_code=401, message=message, error_code="JWT_FAILURE", err=err)
