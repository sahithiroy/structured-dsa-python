import yaml
from fastapi import FastAPI, HTTPException, Response
from pydantic import ValidationError

from open_api import custom_openapi
from src.api.incidents.router import router
from src.middleware.error.exception_handlers import (
    general_exception_handler,
    custom_http_exception_handler,
    http_exception_handler,
    pydantic_validation_exception_handler
)
from src.middleware.error.exceptions import CustomHTTPException

# Initialize the FastAPI application
app = FastAPI()

# Add custom exception handlers for handling different types of exceptions
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)  # For Pydantic validation errors
app.add_exception_handler(HTTPException, http_exception_handler)  # For FastAPI HTTP exceptions
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)  # For custom application exceptions
app.add_exception_handler(Exception, general_exception_handler)  # For unexpected general exceptions

# Set the custom OpenAPI schema generator
app.openapi = custom_openapi

# Include the router for incidents-related endpoints with a specific prefix and tag
app.include_router(router, prefix="/api/v1", tags=["Incidents"])


@app.get("/")
async def home():
    return {"message": "Welcome to Zyrone Energy - BMS Analytics API"}


@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    """
    Endpoint to provide the OpenAPI schema in YAML format.
    This is useful for developers who need the schema in a machine-readable format.

    Returns:
        Response: A YAML representation of the OpenAPI schema.
    """
    # Generate the OpenAPI schema using the custom generator
    openapi_schema = app.openapi()

    # Convert the schema to YAML format
    yaml_schema = yaml.dump(openapi_schema, default_flow_style=False)

    # Return the YAML schema as a response with the appropriate content type
    return Response(content=yaml_schema, media_type="application/x-yaml")
