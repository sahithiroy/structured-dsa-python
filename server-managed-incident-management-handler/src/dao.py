import logging
import traceback
from datetime import datetime, timedelta, UTC, timezone
from typing import Optional, List
from enums import IncidentStatus
from database import Database
from pymongo import ReturnDocument
from model import IncidentAnomaly, Incident


class IncidentsDao:
    """
    A DAO to manage CRUD operations on the incidents model
    """

    def __init__(self, tenant_id: str, tenant_namespace: str):
        self.tenant_id = tenant_id
        self.tenant_namespace = tenant_namespace
        self.INCIDENTS_COLLECTION = "incidents"
        self.INCIDENT_COUNTER_COLLECTION = "incident_counter"
        self.previous_incident_time_delta_in_hours = 3

    def add_new_incident(self, incident: Incident, owner_id: str) -> Optional[Incident]:
        """
        Adds a new incident to the database.

        Args:
            tenant_id (str): The ID of the tenant owning this incident.
            incident (Incident): The incident object to be added.
            owner_id (str):The ID of the user who owns the Incident

        Returns:
            Optional[Incident]: The inserted incident object if successful, or None if an error occurs.
        """
        try:

            # Convert incident to a dictionary with MongoDB-specific structure
            incident_dict = incident.dict(by_alias=True)
            incident_dict["_id"] = incident.id  # Use incident ID as the primary key
            incident_dict["owner_id"] = owner_id

            # Insert the incident into the database
            with Database(self.tenant_namespace) as db:
                db.get_collection(self.INCIDENTS_COLLECTION).insert_one(incident_dict)

            # Log the successful insertion
            logging.info(
                f"[Tenant-{self.tenant_id}] Successfully inserted new incident: {incident.id}"
            )

            return incident
        except Exception as e:
            # Log the error and traceback for debugging
            logging.error(
                f"[Tenant-{self.tenant_id}] Error while inserting new incident: {str(e)} \n {traceback.format_exc()}"
            )
            return None

    def update_incident(
        self,
        incident_id: str,
        status: int,
        owner_id: str,
        stopped_at: Optional[datetime] = None,
        anomalous_kpis: Optional[list[IncidentAnomaly]] = None,
    ) -> Optional[Incident]:
        """
        Updates an existing incident's status and other attributes.

        Args:
            tenant_id (str): The ID of the tenant owning the incident.
            incident_id (str): The unique ID of the incident to update.
            status (int): The new status of the incident.
             owner_id (str):The ID of the user who owns the Incident
            stopped_at (Optional[datetime]): The timestamp when the incident was stopped (if applicable).
            anomalous_kpis (Optional[list[IncidentAnomaly]]): A list of anomalies to append to the incident.

        Returns:
            Optional[Incident]: The updated incident object, or None if the update fails.
        """
        try:
            # Prepare fields to be updated
            set_obj = {"updatedAt": datetime.now(UTC), "status": status}

            # Include stoppedAt if provided
            if stopped_at:
                set_obj["stoppedAt"] = stopped_at

            # Build update object for MongoDB
            update_obj = {"$set": set_obj}

            # Append anomalous KPIs if provided
            if anomalous_kpis:
                push_obj = {
                    "anomalies": {
                        "$each": list(map(lambda x: x.dict(), anomalous_kpis))
                    }
                }
                update_obj["$push"] = push_obj

            # Perform the update operation and retrieve the updated document
            with Database(self.tenant_namespace) as db:
                updated_incident = db.get_collection(
                    self.INCIDENTS_COLLECTION
                ).find_one_and_update(
                    {"incidentId": incident_id, "owner_id": owner_id},
                    update_obj,
                    return_document=ReturnDocument.AFTER,
                )

            if not updated_incident:
                return None

            # Return the updated incident as an object
            return Incident(**updated_incident)
        except Exception as e:
            # Log the error and traceback for debugging
            logging.error(
                f"[Tenant-{self.tenant_id}] Error while updating incident '{incident_id}': {str(e)} \n {traceback.format_exc()}"
            )
            return None

    def update_anomaly_severity_for_given_battery_and_kpi(
        self,
        incident_id: str,
        battery_unit_id: str,
        kpi: str,
        severity: int,
        owner_id: str,
    ) -> bool:
        """
        Updates the anomalies array in the incident document for a specific battery unit, KPI, and owner.

        Args:
            incident_id (str): The ID of the incident.
            battery_unit_id (str): The ID of the battery unit.
            kpi (str): The KPI to update.
            owner_id (str): The ID of the owner.
            new_values (List[float]): The new values to replace null.
            latest_trend (str): The new latest trend to replace null.
            forecast (List[float]): The new forecast to replace null.
            overall_trend (str): The new overall trend to replace null.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            # Define the filter to find the specific incident and anomaly
            filter_query = {
                "incidentId": incident_id,
                "ownerId": owner_id,
                "anomalies": {
                    "$elemMatch": {"batteryUnitId": battery_unit_id, "kpi": kpi}
                },
            }

            # Define the update operation to replace null values
            update_query = {
                "$set": {
                    "anomalies.$.severity": severity,
                    "updatedAt": datetime.now(UTC),
                }
            }
            # Perform the update operation
            with Database(self.tenant_namespace) as db:
                result = db.get_collection(
                    self.INCIDENTS_COLLECTION
                ).find_one_and_update(filter_query, update_query, return_document=True)
            # Check if the update was successful
            if result is not None:
                logging.info(
                    f"Successfully updated anomaly for incident {incident_id}, battery unit {battery_unit_id}, and KPI {kpi}."
                )
                return result
            logging.warning(
                f"No matching anomaly found for incident {incident_id}, battery unit {battery_unit_id}, and KPI {kpi}."
            )
            return None

        except Exception as e:
            logging.error(f"Failed to update anomaly for incident {incident_id}: {e}")
            raise e

    def get_ongoing_or_in_observation_incident(
        self, asset_code: str
    ) -> Optional[Incident]:
        """
        Fetches an existing incident for a given asset code if it exists within the last 3 hours.

        Args:
            asset_code (str): Asset code for which we need to fetch the incident

        Returns:
            The existing incident (if found) or None.
        """
        try:
            # Calculate the time 3 hours ago from the current UTC time
            three_hours_ago = datetime.now(timezone.utc) - timedelta(
                hours=self.previous_incident_time_delta_in_hours
            )
            with Database(self.tenant_namespace) as db:
                existing_incident = db.get_collection(
                    self.INCIDENTS_COLLECTION
                ).find_one(
                    {
                        "assetCode": asset_code,
                        "$or": [
                            {"status": IncidentStatus.ONGOING.value},
                            {
                                "status": IncidentStatus.IN_OBSERVATION.value,
                                "stoppedAt": {
                                    "$gt": three_hours_ago,  # Greater than or equal to 3 hours ago
                                },
                            },
                        ],
                    },
                    sort=[("updatedAt", -1)],
                )

            if not existing_incident:
                return None

            # Return the retrieved incident as an object
            return Incident(**existing_incident)

        except Exception as e:
            # Log the error and traceback for debugging
            logging.error(
                f"[Tenant-{self.tenant_id}] Error while fetching incident for asset '{asset_code}': {str(e)} \n {traceback.format_exc()}"
            )
            return None

    def get_next_incident_id(self, owner_id: str, asset_code: str) -> int:
        """
        Increments the 'incident' field for a given tenantKey and assetCode.
        If no record exists, it creates a new one starting with incident = 1.

        Args:
            tenant_id (str): The tenant key.
            asset_code (str): The asset code.

        Returns:
            IncidentCounterModel: The updated or created document.
        """
        query = {"owner_id": owner_id, "asset_code": asset_code}
        update = {
            "$inc": {"incident": 1},
            "$setOnInsert": {"owner_id": owner_id, "asset_code": asset_code},
        }

        # Use find_one_and_update to atomically increment or insert if not exists
        with Database(self.tenant_namespace) as db:
            result = db.get_collection(
                self.INCIDENT_COUNTER_COLLECTION
            ).find_one_and_update(
                query,
                update,
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )
        return result.get("incident", None)
