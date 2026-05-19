import yaml
from fastapi import FastAPI, HTTPException
from fastapi import Response
from fastapi.openapi.utils import get_openapi
from pydantic import ValidationError
from src.api.cats.router import router
from src.api.dogs.router import router as dog_router
from src.middleware.error.exception_handlers import general_exception_handler, custom_http_exception_handler, \
    http_exception_handler, pydantic_validation_exception_handler
from src.middleware.error.exceptions import CustomHTTPException


# Define your custom OpenAPI schema generator
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Seed application",
        version="1.0.0",
        description="CRUD on CAT Schema and AWS token validation with RBAC",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()

# Add custom exception handlers
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Set the custom OpenAPI schema generator
app.openapi = custom_openapi
app.include_router(router, prefix="/api/v1/cats", tags=["cats"])
app.include_router(dog_router, prefix="/api/v1/dogs", tags=["dogs"])

@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    openapi_schema = app.openapi()
    yaml_schema = yaml.dump(openapi_schema, default_flow_style=False)
    return Response(content=yaml_schema, media_type="application/x-yaml")
