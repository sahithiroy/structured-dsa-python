from typing import Optional

from fastapi import APIRouter, status, Request
from src.api.incidents.model import KPIPayload, Incident
from src.api.incidents.service import IncidentsService
import logging

from src.middleware.auth.cognito_user import CognitoUser


# Initialize logger and router
logging.basicConfig(level=logging.INFO)  # Configures logging to display info-level logs
logger = logging.getLogger(__name__)  # Creates a logger instance for this module

router = APIRouter()  # Creates an API router for managing endpoints in the incidents module


@router.put("/company/{company_id}/incident/report",
            status_code=status.HTTP_201_CREATED)  # Defines a PUT endpoint with HTTP 201 Created status
# @groups_required([UserGroups.AccountAdmin])  # Restricts access to users in the AccountAdmin group
async def incident_handler(request: Request, current_user: Optional[CognitoUser] = None):
    """
    Handles PUT requests for the endpoint.
    - Validates and processes a payload for an incident-related event.
    - Restricts access to users in the AccountAdmin group.

    Args:
        request (Request): The incoming HTTP request containing the payload.
        current_user (Optional[CognitoUser]): The current authenticated user, retrieved from middleware.

    Returns:
        JSON response from the IncidentService after processing the event.
    """
    # Extract the cat ID from the request path parameters
    company_id: str = request.path_params.get("company_id", "")
    payload = await request.json()  # Parses the JSON payload from the incoming request
    kpi_payload = KPIPayload(**payload)  # Validates and converts the JSON payload into a KPIPayload model
    incident_service = IncidentsService(tenant_id=kpi_payload.tenant_id,tenant_namespace=kpi_payload.tenant_namespace,
                                        siteCode=kpi_payload.site_code,assetCode=kpi_payload.asset_code)  # Initializes the IncidentService to handle business logic
    processed: bool = incident_service.process_event(event=kpi_payload, owner_id=company_id)
    return {
        "message": "Successfully initiate processing"
    }
    # Calls the IncidentService to process the event and associates it with the current user's ID
