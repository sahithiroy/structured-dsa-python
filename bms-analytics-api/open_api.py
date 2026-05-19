from fastapi.openapi.utils import get_openapi


def custom_openapi(app):
    """
    Generates a custom OpenAPI schema for the application.
    Adds additional metadata and security configurations for the API documentation.

    Returns:
        dict: The OpenAPI schema with custom configurations.
    """
    # Return the cached schema if already generated
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the base OpenAPI schema
    openapi_schema = get_openapi(
        title="Incident application",  # Title of the API documentation
        version="1.0.0",  # API version
        description="Incident and AWS token validation with RBAC",  # Description of the API
        routes=app.routes,  # Routes to include in the schema
    )

    # Add security scheme for Bearer Authentication (JWT)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",  # HTTP-based authentication
            "scheme": "bearer",  # Bearer token scheme
            "bearerFormat": "JWT"  # Specify the token format (JSON Web Token)
        }
    }

    # Define global security requirements for all routes
    openapi_schema["security"] = [{"BearerAuth": []}]

    # Cache the schema for future use
    app.openapi_schema = openapi_schema
    return app.openapi_schema
