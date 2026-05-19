import logging
from datetime import datetime, UTC
from typing import Optional
from enums import BatteryKPI, IncidentStatus, BatteryNames, AlertCategory
from model import KPIPayload, Incident, IncidentAnomaly
from data_dao import IncidentData
from alerts_service import AlertsService
from dao import IncidentsDao

logging.basicConfig(level=logging.INFO)  # Set logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(p_event: any, context):
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
    logging.info(f"Received event: {p_event}")
    detail = p_event.get("detail", {})
    payload = detail.get("payload", {})
    logging.info(f"Extracted payload: {payload}")
    if not payload:  # Check if detail exists
        logging.error("Missing 'payload' field in event payload")
        return {"error": "Missing 'payload' field in event payload"}
    if len(payload) == 0:  # Check if detail exists
        logging.error("'payload' list is empty")
        return {"error": "Missing 'payload' field in event payload"}

    kpi_payload_list = list(map(lambda p: KPIPayload(**p), payload))

    incident_service = IncidentsService(
        tenant_id=kpi_payload_list[0].tenant_id,
        tenant_namespace=kpi_payload_list[0].tenant_namespace,
        siteCode=kpi_payload_list[0].site_code,
        assetCode=kpi_payload_list[0].asset_code,
    )  # Initializes the IncidentService to handle business logic

    incident_service.process_event(
        events=kpi_payload_list, owner_id=kpi_payload_list[0].tenant_id
    )
    return {"message": "Successfully initiate processing"}


class IncidentsService:

    def __init__(
        self, tenant_id: str, tenant_namespace: str, siteCode: str, assetCode: str
    ):
        """
        Initialize the Service with a DAO instance.
        """
        self.dao = IncidentsDao(tenant_id, tenant_namespace)
        self.incident_data = IncidentData(tenant_namespace, siteCode, assetCode)

    def process_event(self, events: list[KPIPayload], owner_id: str) -> bool:
        """
        Processes an event to determine the state transition of an asset's error status.

        The function handles transitions in the error state (`e_state`) of an asset based on the
        current and previous states. It logs appropriate messages and invokes state transition
        functions based on the type of state change.

        Args:
            events (list[KPIPayload]): An object containing the details of the current and previous state
                                of an asset, including tenant information and asset-specific details.
            owner_id (str): The ID of the user who owns the Incident

        Returns:
            dict: A dictionary containing a status code and message with alerts and incident details.
        """

        existing_incident: Optional[Incident] = self.get_existing_incident(
            asset_code=events[0].asset_code
        )
        next_incident_id: str = self.generate_next_incident_id(
            existing_incident, asset_code=events[0].asset_code
        )

        #
        # ================
        # Process each received kpi event
        # ================
        #
        for event in events:

            # Check if the event indicates a new error starting (state changes from 'Normal' to 'Error').
            if event.prev.e_state == "N" and event.now.e_state == "E":
                logging.info(
                    f"[Tenant-{owner_id}][{event.asset_code}][{event.battery_unit_id}] New error started for asset '{event.asset_code}'"
                )
                try:
                    # Handle the transition from normal state ('N') to error state ('E').
                    self.state_transition_normal_to_error(
                        payload_event=event,
                        owner_id=owner_id,
                        existing_incident=existing_incident,
                        next_incident_id=next_incident_id,
                    )
                    return True
                except Exception as e:
                    logging.info(
                        f"[Tenant-{owner_id}][{event.asset_code}][{event.battery_unit_id}] Error while handling a new error started for asset '{event.asset_code}'"
                    )
                    return False
                # Get the anomalous KPIs to mention in the message
            # Check if the event indicates an ongoing error (state remains 'Error').
            elif event.prev.e_state == "E" and event.now.e_state == "E":
                logging.info(
                    f"[Tenant-{owner_id}][{event.asset_code}][{event.battery_unit_id}] Ongoing error continues for asset '{event.asset_code}'"
                )
                try:
                    # Handle the transition when the state remains in error ('E').
                    self.state_transition_error_to_error(
                        payload_event=event,
                        owner_id=owner_id,
                        existing_incident=existing_incident,
                        next_incident_id=next_incident_id,
                    )
                    # Get the anomalous KPIs to mention in the message
                    return True
                except Exception as e:
                    logging.info(
                        f"[Tenant-{owner_id}][{event.asset_code}][{event.battery_unit_id}] Error while handling an ongoing error continues for asset '{event.asset_code}'"
                    )
                    return False

            # Check if the event indicates an error stopping (state changes from 'Error' to 'Normal').
            elif event.prev.e_state == "E" and event.now.e_state == "N":
                logging.info(
                    f"[Tenant-{owner_id}][{event.asset_code}][{event.battery_unit_id}] An ongoing error stopped for asset '{event.asset_code}'"
                )
                # Handle the transition from error state ('E') to normal state ('N').
                try:
                    self.state_transition_error_to_normal(
                        payload_event=event,
                        owner_id=owner_id,
                        existing_incident=existing_incident,
                    )
                    return True
                except Exception as e:
                    logging.info(
                        f"[Tenant-{owner_id}][{event.asset_code}][{event.battery_unit_id}] Error while handling an ongoing error stopped for asset '{event.asset_code}'"
                    )
                    return False

            # If the state is normal and there is no relevant transition, log an informational message.
            else:
                logging.info(
                    f"[Tenant-{event.tenant_namespace}][{event.asset_code}][{event.battery_unit_id}] Normal state for asset '{event.asset_code}'. Ignore request"
                )
                return True

        return True

    def get_existing_incident(self, asset_code: str):
        # Check if any previous existing incident for this asset
        existing_incident: Optional[Incident] = (
            self.dao.get_ongoing_or_in_observation_incident(asset_code=asset_code)
        )
        return existing_incident

    def generate_next_incident_id(
        self, existing_incident: Optional[Incident], asset_code: str
    ):

        # If incident exists
        if existing_incident:
            # Extract the last incident number
            current_incident_number = int(
                existing_incident.incidentId.replace(f"INC-{asset_code.upper()}-", "")
            )
        else:
            current_incident_number = 0

        # Return the next incident id
        return f"INC-{asset_code.upper()}-{current_incident_number+1}"

    def state_transition_normal_to_error(
        self,
        payload_event: KPIPayload,
        owner_id: str,
        existing_incident: Optional[Incident],
        next_incident_id: str,
    ) -> Optional[Incident]:
        """
        Handles the transition of an asset's state from 'Normal' to 'Error' by managing incidents.
        It checks for existing incidents and either updates them or creates a new one if none exist.

        Args:
            payload_event (KPIPayload): The payload containing event details such as tenant info,
                                        asset details, and anomaly data.
            owner_id (str): The ID of the user who owns the incident.
            existing_incident (Incident): Previous existing incident for this asset
            next_incident_id(int): Unique number for the next incident for this asset

        Returns:
            Optional[Incident]: The updated or newly created incident object, or None if no action was needed.
        """

        # Identify current anomalous KPIs that should trigger an alert.
        now_anomalous_kpi_names: list[str] = self.create_alerts_for_anomalous_kpis(
            owner_id=owner_id, event=payload_event
        )

        # Check if there is an ongoing or in-observation incident for the asset.
        logging.info(
            f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Checking ongoing or in-observation incidents for asset '{payload_event.asset_code}'"
        )

        # If an incident exists, update it with the new anomalies.
        if existing_incident:
            logging.info(
                f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Found existing incident: '{existing_incident.incidentId}'"
            )

            # Determine if the incident is ongoing or in observation.
            incident_type = (
                "ongoing" if existing_incident.status == 0 else "in-observation"
            )

            # Extract the KPIs currently associated with the incident for the relevant battery and bank unit.
            current_battery_existing_anomalous_kpi_names: list[str] = list(
                map(
                    lambda anomaly: anomaly.kpi,
                    filter(
                        lambda anomaly: (
                            anomaly.batteryUnitId == payload_event.battery_unit_id
                            or anomaly.batteryUnitId == BatteryNames.BATTERIES.value
                        )
                        and anomaly.bankUnitId == payload_event.bank_unit_id,
                        existing_incident.anomalies,
                    ),
                )
            )
            # Iterate through the list of KPIs that are already part of the existing incident and require updates.
            for kpi_name in current_battery_existing_anomalous_kpi_names:

                # Fetch the anomaly object corresponding to the kpi
                kpi_anomaly_objects: list[IncidentAnomaly] = list(
                    filter(
                        lambda a: a.kpi == kpi_name
                        and (
                            a.batteryUnitId == payload_event.battery_unit_id
                            or a.batteryUnitId == BatteryNames.BATTERIES.value
                        ),
                        existing_incident.anomalies,
                    )
                )
                kpi_anomaly_object: Optional[IncidentAnomaly] = (
                    kpi_anomaly_objects[0] if len(kpi_anomaly_objects) > 0 else None
                )
                if kpi_anomaly_object:
                    # If the received KPI is for charge current (Bank level) and now is reporting a severity level different
                    # from previously reported value => add it to the anomaly list else ignore
                    if (
                        kpi_anomaly_object.kpi == BatteryKPI.CURRENT.value
                        and payload_event.now.ci_as == kpi_anomaly_object.severity
                        and kpi_anomaly_object.batteryUnitId
                        == BatteryNames.BATTERIES.value
                    ):
                        logging.info(
                            f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Skipping update for KPI '{kpi_name}' as update_current_bank_level returned False."
                        )
                        continue
                    # Update the incident with anomaly details
                    self.dao.update_anomaly_severity_for_given_battery_and_kpi(
                        incident_id=existing_incident.incidentId,  # Incident ID of the existing anomaly.
                        battery_unit_id=self.get_battery_name_by_kpi(
                            kpi_name, payload_event
                        ),
                        # Get the battery unit ID.
                        kpi=kpi_name,  # KPI name.
                        severity=self.get_severity(
                            kpi_name, payload_event
                        ),  # Determine the new severity.
                        owner_id=owner_id,  # Owner ID responsible for this anomaly.
                    )

            # Identify new KPIs that were not previously part of the incident.
            to_add_anomalous_kpi_names = list(
                filter(
                    lambda x: x not in current_battery_existing_anomalous_kpi_names,
                    now_anomalous_kpi_names,
                )
            )
            # Prepare new anomaly objects if there are new anomalous KPIs.
            to_add_anomalous_objects = []
            for kpi_name in to_add_anomalous_kpi_names:
                # Create an IncidentAnomaly object for each new anomalous KPI.
                to_add_anomalous_objects.append(
                    IncidentAnomaly(
                        kpi=kpi_name,
                        values=[],  # anomaly_values,
                        severity=self.get_severity(kpi_name, payload_event),
                        batteryUnitId=self.get_battery_name_by_kpi(
                            kpi_name, payload_event
                        ),
                        bankUnitId=payload_event.bank_unit_id,
                        latestTrend="",  # data_trends_and_forecast.latest_trend,
                        overallTrend="",  # data_trends_and_forecast.overall_trend,
                        forecast=[],  # data_trends_and_forecast.forecast
                    )
                )

            # Log the update process.
            logging.info(
                f"[Tenant-{owner_id}] Updating {incident_type} incident '{existing_incident.incidentId}' for asset '{payload_event.asset_code}'"
            )

            # Update the existing incident in the database with new anomalies and set its status to 'ongoing'.
            return self.dao.update_incident(
                incident_id=existing_incident.incidentId,
                status=IncidentStatus.ONGOING.value,
                owner_id=owner_id,
                anomalous_kpis=(
                    to_add_anomalous_objects if to_add_anomalous_objects else None
                ),
            )

        # If no existing incident is found, create a new incident.
        else:
            logging.info(
                f"[Tenant-{owner_id}] Creating a new incident for asset '{payload_event.asset_code}'"
            )

            # Create new anomaly objects for the incident.
            new_anomalous_kpis = [
                IncidentAnomaly(
                    kpi=kpi_name,
                    severity=self.get_severity(kpi_name, payload_event),
                    batteryUnitId=self.get_battery_name_by_kpi(kpi_name, payload_event),
                    bankUnitId=payload_event.bank_unit_id,
                )
                for kpi_name in now_anomalous_kpi_names
            ]

            # Create a new incident object.
            new_incident = Incident(
                status=IncidentStatus.ONGOING.value,  # Set status to 'ongoing'
                startedAt=datetime.now(UTC),  # Record the start time of the incident
                assetCode=payload_event.asset_code,  # Set asset identifier
                anomalies=new_anomalous_kpis,  # Attach identified anomalies
                incidentId=next_incident_id,  # Generate unique incident ID
                ownerId=owner_id,  # Assign the incident to the tenant
                createdAt=datetime.now(UTC),  # Record the creation timestamp
                updatedAt=datetime.now(UTC),  # Record the last update timestamp
            )

            # Add the new incident to the database and return it.
            return self.dao.add_new_incident(incident=new_incident, owner_id=owner_id)

    def state_transition_error_to_error(
        self,
        payload_event: KPIPayload,
        owner_id: str,
        existing_incident: Optional[Incident],
        next_incident_id: str,
    ) -> Optional[Incident]:
        """
        Handles the transition of an asset from one error state to another, updating or creating incidents
        as necessary based on the severity of KPI anomalies.

        Args:
            payload_event (KPIPayload): Contains tenant, asset, and anomaly details for the event.
            owner_id (str): The ID of the user who owns the Incident.
            existing_incident (Incident): Previous existing incident for this asset
            next_incident_id(int): Unique number for the next incident for this asset

        Returns:
            Optional[Incident]: The updated or newly created Incident, or None if no changes are made.
        """

        # Identify KPIs with severity changes based on the payload.
        severity_changed_kpi_names: list[str] = (
            self.create_alerts_for_severity_changed_anomalous_kpis(
                owner_id=owner_id, event=payload_event
            )
        )
        logging.info(
            f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Severities changed for Kpis : {severity_changed_kpi_names}"
        )

        #
        # If there are KPIs with severity changes, update an existing incident or create a new one.
        #
        if len(severity_changed_kpi_names) > 0:

            if existing_incident:
                # Extract KPIs already marked as anomalous in the existing incident for the same battery and bank unit.
                current_battery_existing_anomalous_kpi_names: list[str] = list(
                    map(
                        lambda x: x.kpi,
                        filter(
                            lambda y: (
                                y.batteryUnitId == payload_event.battery_unit_id
                                or y.batteryUnitId == BatteryNames.BATTERIES.value
                            )
                            and y.bankUnitId == payload_event.bank_unit_id,
                            existing_incident.anomalies or [],
                        ),
                    )
                )
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Anomalous kpis of the current battery : {current_battery_existing_anomalous_kpi_names}"
                )

                # Iterate through the list of KPIs that are already part of the existing incident and require updates.
                for kpi_name in current_battery_existing_anomalous_kpi_names:

                    # Fetch the anomaly object corresponding to the kpi
                    kpi_anomaly_objects: list[IncidentAnomaly] = list(
                        filter(
                            lambda a: a.kpi == kpi_name
                            and (
                                a.batteryUnitId == payload_event.battery_unit_id
                                or a.batteryUnitId == BatteryNames.BATTERIES.value
                            ),
                            existing_incident.anomalies,
                        )
                    )
                    kpi_anomaly_object: Optional[IncidentAnomaly] = (
                        kpi_anomaly_objects[0] if len(kpi_anomaly_objects) > 0 else None
                    )
                    if kpi_anomaly_object:
                        # If the received KPI is for charge current (Bank level) and now is reporting a severity level different
                        # from previously reported value => add it to the anomaly list else ignore
                        if (
                            kpi_anomaly_object.kpi == BatteryKPI.CURRENT.value
                            and payload_event.now.ci_as == kpi_anomaly_object.severity
                            and kpi_anomaly_object.batteryUnitId
                            == BatteryNames.BATTERIES.value
                        ):
                            logging.info(
                                f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Skipping update for KPI '{kpi_name}' as update_current_bank_level returned False."
                            )
                            continue
                        # Update the incident with anomaly details
                        self.dao.update_anomaly_severity_for_given_battery_and_kpi(
                            incident_id=existing_incident.incidentId,  # Incident ID of the existing anomaly.
                            battery_unit_id=self.get_battery_name_by_kpi(
                                kpi_name, payload_event
                            ),
                            # Get the battery unit ID.
                            kpi=kpi_name,  # KPI name.
                            severity=self.get_severity(
                                kpi_name, payload_event
                            ),  # Determine the new severity.
                            owner_id=owner_id,  # Owner ID responsible for this anomaly.
                        )

                # Determine new KPIs that need to be added to the existing incident.
                to_add_anomalous_kpi_names = list(
                    filter(
                        lambda x: x not in current_battery_existing_anomalous_kpi_names,
                        severity_changed_kpi_names,
                    )
                )
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Add new set of severities reported that does not exist in incident : {to_add_anomalous_kpi_names}"
                )

                # Prepare new anomaly objects if there are new anomalous KPIs.
                to_add_anomalous_objects = []
                for kpi_name in to_add_anomalous_kpi_names:
                    # Create an IncidentAnomaly object for each new anomalous KPI.
                    to_add_anomalous_objects.append(
                        IncidentAnomaly(
                            kpi=kpi_name,
                            values=[],  # anomaly_values,
                            severity=self.get_severity(kpi_name, payload_event),
                            batteryUnitId=self.get_battery_name_by_kpi(
                                kpi_name, payload_event
                            ),
                            bankUnitId=payload_event.bank_unit_id,
                            latestTrend="",  # data_trends_and_forecast.latest_trend,
                            overallTrend="",  # data_trends_and_forecast.overall_trend,
                            forecast=[],  # data_trends_and_forecast.forecast
                        )
                    )

                # Update the existing incident in the database, setting it to "ongoing."
                result = self.dao.update_incident(
                    incident_id=existing_incident.incidentId,
                    status=IncidentStatus.ONGOING.value,  # Ensure status remains ongoing.
                    anomalous_kpis=to_add_anomalous_objects,
                    stopped_at=None,
                    owner_id=owner_id,
                )
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Successfully updated the existing incident with new kpi severities : {existing_incident.incidentId}"
                )
                return result
            #
            # If no existing incident found => create one now
            #
            else:
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Create new incident"
                )

                # Identify all currently anomalous KPIs.
                now_anomalous_kpi_names: list[str] = (
                    self.create_alerts_for_anomalous_kpis(
                        owner_id=owner_id, event=payload_event, create_alert=False
                    )
                )
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Create alerts for kpis : {now_anomalous_kpi_names}"
                )

                # Create IncidentAnomaly objects for new KPIs.
                new_anomalous_kpis = list(
                    map(
                        lambda x: IncidentAnomaly(
                            kpi=x,
                            severity=self.get_severity(x, payload_event),
                            batteryUnitId=self.get_battery_name_by_kpi(
                                x, payload_event
                            ),
                            bankUnitId=payload_event.bank_unit_id,
                        ),
                        now_anomalous_kpi_names,
                    )
                )

                # Create a new Incident object.
                new_incident = Incident(
                    status=IncidentStatus.ONGOING.value,
                    startedAt=datetime.now(UTC),
                    assetCode=payload_event.asset_code,
                    anomalies=new_anomalous_kpis,
                    incidentId=next_incident_id,
                    ownerId=owner_id,
                    createdAt=datetime.now(UTC),
                    updatedAt=datetime.now(UTC),
                    stoppedAt=None,
                )

                # Add the new incident to the database.
                result = self.dao.add_new_incident(
                    incident=new_incident, owner_id=owner_id
                )
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Successfully created a new incident with id - {next_incident_id}"
                )
                return result
        #
        # If no severity changed for any of the kpi
        #
        else:
            logging.info(
                f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] No severity levels changed for any KPI"
            )

            if existing_incident:

                # Extract KPIs already marked as anomalous in the existing incident for the same battery and bank unit.
                current_battery_existing_anomalous_kpi_names: list[str] = list(
                    map(
                        lambda x: x.kpi,
                        filter(
                            lambda y: (
                                y.batteryUnitId == payload_event.battery_unit_id
                                or y.batteryUnitId == BatteryNames.BATTERIES.value
                            )
                            and y.bankUnitId == payload_event.bank_unit_id,
                            existing_incident.anomalies or [],
                        ),
                    )
                )

                # Iterate through the list of KPIs that are already part of the existing incident and require updates.
                for kpi_name in current_battery_existing_anomalous_kpi_names:

                    # Fetch the anomaly object corresponding to the kpi
                    kpi_anomaly_objects: list[IncidentAnomaly] = list(
                        filter(
                            lambda a: a.kpi == kpi_name
                            and (
                                a.batteryUnitId == payload_event.battery_unit_id
                                or a.batteryUnitId == BatteryNames.BATTERIES.value
                            ),
                            existing_incident.anomalies,
                        )
                    )
                    kpi_anomaly_object: Optional[IncidentAnomaly] = (
                        kpi_anomaly_objects[0] if len(kpi_anomaly_objects) > 0 else None
                    )
                    if kpi_anomaly_object:
                        # If the received KPI is for charge current (Bank level) and now is reporting a severity level different
                        # from previously reported value => add it to the anomaly list else ignore
                        if (
                            kpi_anomaly_object.kpi == BatteryKPI.CURRENT.value
                            and payload_event.now.ci_as == kpi_anomaly_object.severity
                            and kpi_anomaly_object.batteryUnitId
                            == BatteryNames.BATTERIES.value
                        ):
                            logging.info(
                                f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Skipping update for KPI '{kpi_name}' as update_current_bank_level returned False."
                            )
                            continue
                        # Update the incident with anomaly details
                        self.dao.update_anomaly_severity_for_given_battery_and_kpi(
                            incident_id=existing_incident.incidentId,  # Incident ID of the existing anomaly.
                            battery_unit_id=self.get_battery_name_by_kpi(
                                kpi_name, payload_event
                            ),
                            # Get the battery unit ID.
                            kpi=kpi_name,  # KPI name.
                            severity=self.get_severity(
                                kpi_name, payload_event
                            ),  # Determine the new severity.
                            owner_id=owner_id,  # Owner ID responsible for this anomaly.
                        )
                return existing_incident
            #
            # If there is no existing incident, create a new one.
            #
            else:
                logging.info(
                    f"[Tenant-{owner_id}][{payload_event.asset_code}][{payload_event.battery_unit_id}] Creating new incident for asset '{payload_event.asset_code}'"
                )

                # Identify currently anomalous KPIs.
                now_anomalous_kpi_names: list[str] = (
                    self.create_alerts_for_anomalous_kpis(
                        owner_id=owner_id, event=payload_event, create_alert=False
                    )
                )

                # Create IncidentAnomaly objects for the detected anomalies.
                new_anomalous_kpis = list(
                    map(
                        lambda x: IncidentAnomaly(
                            kpi=x,
                            severity=self.get_severity(x, payload_event),
                            batteryUnitId=self.get_battery_name_by_kpi(
                                x, payload_event
                            ),
                            bankUnitId=payload_event.bank_unit_id,
                        ),
                        now_anomalous_kpi_names,
                    )
                )

                # Generate a new unique incident ID.
                # next_incident_id = self.dao.get_next_incident_id(
                #     owner_id, payload_event.asset_code
                # )

                # Create a new Incident object with the detected anomalies.
                new_incident = Incident(
                    status=IncidentStatus.ONGOING.value,
                    startedAt=datetime.now(UTC),
                    assetCode=payload_event.asset_code,
                    anomalies=new_anomalous_kpis,
                    incidentId=next_incident_id,
                    ownerId=owner_id,
                    createdAt=datetime.now(UTC),
                    updatedAt=datetime.now(UTC),
                    stoppedAt=None,
                )

                # Save the new incident to the database.
                return self.dao.add_new_incident(
                    incident=new_incident, owner_id=owner_id
                )

    def state_transition_error_to_normal(
        self,
        payload_event: KPIPayload,
        owner_id: str,
        existing_incident: Optional[Incident],
    ) -> Optional[Incident]:
        """
        Handles the transition of an asset's state from an error to a normal condition by updating the incident status.

        Args:
            payload_event (KPIPayload): The payload containing tenant, asset, and anomaly details for the event.
            owner_id (str):The ID of the user who owns the Incident
            existing_incident (Incident): Previous existing incident for this asset

        Returns:
            Optional[Incident]: The updated Incident if one exists, otherwise None.
        """
        # Initialize the DAO for incident operations using the tenant information from the payload.

        # Fetch an ongoing or in-observation incident related to the asset from the database.
        # existing_incident: Incident = self.dao.get_ongoing_or_in_observation_incident(
        #     asset_code=payload_event.asset_code
        # )

        # If an existing incident is found, update its status to "in observation" and record the stop time.
        if existing_incident:
            return self.dao.update_incident(
                incident_id=existing_incident.incidentId,  # The unique identifier for the ongoing incident.
                status=IncidentStatus.IN_OBSERVATION.value,
                # Change the status to "in observation."
                stopped_at=datetime.now(
                    UTC
                ),  # Record the current timestamp as the stop time for the incident.
                owner_id=owner_id,
            )

        # If no incident is found, return None to indicate no update was made.
        return existing_incident

    def create_alerts_for_anomalous_kpis(
        self, owner_id: str, event: KPIPayload, create_alert: bool = True
    ) -> list[str]:
        """
        Creates incidents for KPIs that have been flagged as anomalous based on the provided event data.

        Args:
            owner_id: Id of the company
            event (KPIPayload): The payload containing current and previous KPI data,
                                along with metadata such as asset, site, and tenant details.
            create_alert: Flag that determines whether or not to create alert

        Returns:
            None: This function processes the event and logs or triggers incidents for detected anomalies.

        Raises:
            Any exception occurring during processing will be logged for further debugging.
        """

        # Initialize the alert service with the asset code and tenant ID.
        alerts_service = AlertsService(
            asset_code=event.asset_code, tenant_id=owner_id, site_code=event.site_code
        )

        # List to store the names of KPIs that are flagged as anomalous.
        anomalous_kpi_names: list[str] = []

        # Check if the voltage anomaly score (`v_as`) is greater than 0, indicating an anomaly in voltage.
        if event.now.v_as or 0 > 0:
            # Append the 'Voltage' KPI name to the list of anomalies.
            anomalous_kpi_names.append(BatteryKPI.VOLTAGE.value)

            # If `create_alert` is True, create an alert for the voltage anomaly.
            if create_alert:
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.VOLTAGE.value,
                    value={
                        BatteryKPI.VOLTAGE.value: event.now.v,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.v_as,
                    category=AlertCategory.BATTERY.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )

        # Check if the charging current (`ci_as`) or discharging current (`di_as`) anomaly score is greater than 0.
        if (event.now.ci_as or 0) > 0:
            existing_incident: Optional[Incident] = (
                self.dao.get_ongoing_or_in_observation_incident(
                    asset_code=event.asset_code
                )
            )
            # Append the 'Current' KPI name to the list of anomalies.
            anomalous_kpi_names.append(BatteryKPI.CURRENT.value)
            voltage = self.incident_data.read_bank_voltage()

            # Get the existing anomalies from the incident
            existing_Incident_anomaly = (
                existing_incident.anomalies if existing_incident else []
            )

            # Extract bankUnitId and kpi values from existing anomalies
            bank_unit_ids = [
                anomaly.bankUnitId for anomaly in existing_Incident_anomaly
            ]
            kpi_values = [anomaly.kpi for anomaly in existing_Incident_anomaly]

            # Extract the severity of the 'Current' anomaly (if it exists).
            current_anomaly_severity = None
            for anomaly in existing_Incident_anomaly:
                if (
                    anomaly.kpi == BatteryKPI.CURRENT.value
                ):  # Check if the anomaly is for 'Current'.
                    current_anomaly_severity = anomaly.severity

            # Check if there is no anomaly with the same bank_unit_id and kpi value in the existing incident
            if create_alert and (
                (
                    event.bank_unit_id not in bank_unit_ids
                    and BatteryKPI.CURRENT.value not in kpi_values
                )
                or (current_anomaly_severity != event.now.ci_as)
            ):
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.CURRENT.value,
                    value={
                        BatteryKPI.VOLTAGE.value: voltage,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.ci_as,
                    category=AlertCategory.BANK.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )
        if (event.now.di_as or 0) > 0:
            # Append the 'Current' KPI name to the list of anomalies.
            anomalous_kpi_names.append(BatteryKPI.CURRENT.value)

            # If `create_alert` is True, create an alert for the current anomaly.
            if create_alert:
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.CURRENT.value,
                    value={
                        BatteryKPI.VOLTAGE.value: event.now.v,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.di_as,
                    category=AlertCategory.BATTERY.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )
        # already tested of SOC
        # Check if the state of charge (`soc_as`) anomaly score is greater than 0.
        if event.now.soc_as or 0 > 0:
            # Append the 'State of Charge' KPI name to the list of anomalies.
            anomalous_kpi_names.append(BatteryKPI.STATE_OF_CHARGE.value)

            # If `create_alert` is True, create an alert for the state of charge anomaly.
            if create_alert:
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.STATE_OF_CHARGE.value,
                    value={
                        BatteryKPI.VOLTAGE.value: event.now.v,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.soc_as,
                    category=AlertCategory.BATTERY.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )

        # Return the list of anomalous KPI names.
        return anomalous_kpi_names

    def create_alerts_for_severity_changed_anomalous_kpis(
        self, owner_id: str, event: KPIPayload, create_alert: bool = True
    ) -> list[str]:
        """
        Creates incidents for KPIs that have the severity levels changes when compared to its previous value

        Args:
            event (KPIPayload): The payload containing current and previous KPI data,
                                along with metadata such as asset, site, and tenant details.
            create_alert: Determines whether to create an alert or no

        Returns:
            None: This function processes the event and logs or triggers incidents for detected anomalies.

        Raises:
            Any exception occurring during processing will be logged for further debugging.
        """
        # Initialize the alert service with the asset code and tenant ID from the event.
        alerts_service = AlertsService(
            asset_code=event.asset_code, tenant_id=owner_id, site_code=event.site_code
        )

        # List to store the names of KPIs whose severity levels have changed.
        severity_changed_kpi_names: list[str] = []

        # Check if the severity level for 'Voltage' has changed between current and previous events.
        if (event.now.v_as or 0) != (event.prev.v_as or 0):
            # Add 'Voltage' KPI to the list of severity-changed KPIs.
            severity_changed_kpi_names.append(BatteryKPI.VOLTAGE.value)

            # If the current severity level for 'Voltage' is greater than 0 and alert creation is enabled, create an alert.
            if (event.now.v_as or 0) > 0 and create_alert:
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.VOLTAGE.value,
                    value={
                        BatteryKPI.VOLTAGE.value: event.now.v,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.v_as,
                    category=AlertCategory.BATTERY.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )

        # Check if the severity levels for 'Charging Current' or 'Discharging Current' have changed.
        if (event.now.ci_as or 0) != (event.prev.ci_as or 0):

            # Add 'Current' KPI to the list of severity-changed KPIs.
            severity_changed_kpi_names.append(BatteryKPI.CURRENT.value)

            # Fetch the existing ongoing or in-observation incident.
            existing_incident: Optional[Incident] = (
                self.dao.get_ongoing_or_in_observation_incident(
                    asset_code=event.asset_code
                )
            )

            # Get the existing anomalies from the incident.
            existing_incident_anomalies = (
                existing_incident.anomalies if existing_incident else []
            )

            # Extract the severity of the 'Current' anomaly (if it exists).
            current_anomaly_severity = None
            for anomaly in existing_incident_anomalies:
                if (
                    anomaly.kpi == BatteryKPI.CURRENT.value
                    and anomaly.batteryUnitId == BatteryNames.BATTERIES.value
                ):  # Check if the anomaly is for 'Current'.
                    current_anomaly_severity = anomaly.severity

            # If the severity of 'Charging Current' has changed and is greater than 0, create an alert.
            if (
                (event.now.ci_as or 0) > 0
                and create_alert
                and current_anomaly_severity != event.now.ci_as
            ):
                # Fetch the bank voltage for the alert.
                voltage = self.incident_data.read_bank_voltage()
                # Create a new alert.
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.CURRENT.value,
                    value={
                        BatteryKPI.VOLTAGE.value: voltage,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.ci_as,
                    category=AlertCategory.BANK.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )

        if (event.now.di_as or 0) != (event.prev.di_as or 0):
            # Add 'Current' KPI to the list of severity-changed KPIs.
            severity_changed_kpi_names.append(BatteryKPI.CURRENT.value)
            if ((event.now.di_as or 0) > 0) and create_alert:
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.CURRENT.value,
                    value={
                        BatteryKPI.VOLTAGE.value: event.now.v,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.di_as,
                    category=AlertCategory.BATTERY.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )
        # alreay tested of SOC
        # Check if the severity level for 'State of Charge' has changed between current and previous events.
        if (event.now.soc_as or 0) != (event.prev.soc_as or 0):
            # Add 'State of Charge' KPI to the list of severity-changed KPIs.
            severity_changed_kpi_names.append(BatteryKPI.STATE_OF_CHARGE.value)

            # If the current severity level for 'State of Charge' is greater than 0 and alert creation is enabled, create an alert.
            if (event.now.soc_as or 0) > 0 and create_alert:
                alerts_service.create_alert(
                    tenant_id=owner_id,
                    kpi=BatteryKPI.STATE_OF_CHARGE.value,
                    value={
                        BatteryKPI.VOLTAGE.value: event.now.v,
                        BatteryKPI.CURRENT.value: event.now.i,
                        BatteryKPI.STATE_OF_CHARGE.value: event.now.soc,
                    },
                    severity=event.now.soc_as,
                    category=AlertCategory.BATTERY.value,
                    battery_unit_id=event.battery_unit_id,
                    bank_unit_id=event.bank_unit_id,
                )

        # Return the list of KPI names where severity levels have changed.
        return severity_changed_kpi_names

    def get_severity(self, kpi_name: str, payload_event: KPIPayload) -> Optional[int]:
        """
        Determines the severity of an anomaly based on the given KPI name and the payload event.

        Parameters:
        - kpi_name (str): The name of the KPI ('v' for voltage, 'i' for current, 'soc' for state of charge).
        - payload_event (KPIPayload): The event payload containing anomaly severity values.

        Returns:
        - Optional[int]: The severity value for the given KPI, or None if the KPI is not recognized.
        """
        severity = None  # Default severity value

        if kpi_name == BatteryKPI.VOLTAGE.value:  # Voltage anomaly
            severity = payload_event.now.v_as

        elif kpi_name == BatteryKPI.CURRENT.value:  # Current anomaly
            if payload_event.now.ci_as > 0:  # Charging current anomaly
                severity = payload_event.now.ci_as
            if (
                payload_event.now.di_as > 0
            ):  # Discharging current anomaly (overwrites ci_as if both exist)
                severity = payload_event.now.di_as

        elif kpi_name == BatteryKPI.STATE_OF_CHARGE.value:  # State of charge anomaly
            severity = payload_event.now.soc_as
        else:
            severity = 0

        return severity  # Returns the severity value or None if KPI is not recognized

    def get_battery_name_by_kpi(
        self, kpi_name: str, payload_event: KPIPayload
    ) -> Optional[str]:
        """
        Determines the appropriate battery unit ID based on the KPI name and payload event.

        Args:
            kpi_name (str): The name of the KPI (e.g., 'i' for current).
            payload_event (KPIPayload): The payload event containing KPI data and metadata.

        Returns:
            Optional[str]: The battery unit ID if applicable, otherwise None.
        """
        # If the current anomaly status (ci_as) is greater than 0, set battery_id to None.
        return (
            BatteryNames.BATTERIES.value
            if kpi_name == BatteryKPI.CURRENT.value and payload_event.now.ci_as > 0
            else payload_event.battery_unit_id
        )