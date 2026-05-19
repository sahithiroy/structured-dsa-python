from datetime import datetime

import requests  # Imports the requests library to make HTTP requests
import logging  # Imports the logging module to log information and errors
from config import ALERT_BASE_URL


class AlertsService:
    def __init__(self, asset_code: str, tenant_id: str, site_code: str):
        """
        Initializes the AlertsService class with asset and tenant information.

        Args:
            asset_code (str): The code associated with the asset.
            tenant_id (str): The ID of the tenant that owns the asset.
        """
        self.url = f"{ALERT_BASE_URL}/api/v1/company/{tenant_id}/validate-rule-engine"
        self.asset_code = asset_code  # Stores the asset code for alert creation
        self.tenant_id = tenant_id  # Stores the tenant ID for identifying which tenant is generating the alert
        self.site_code = site_code

    def create_alert(self, tenant_id: str, kpi: str, value: dict, battery_unit_id:str |None, bank_unit_id: str,
                     severity: int, category: int) -> bool:
        """
        Creates an alert by sending a POST request with the provided KPI and asset information.

        Args:
            category: Category of the alert
            severity: Severity of the alert
            tenant_id (str): The tenant ID responsible for the alert.
            kpi (str): The key performance indicator for the alert.
            value (float): The value of the KPI that triggered the alert.|None
            battery_unit_id (str): The ID of the battery unit associated with the alert.
            bank_unit_id (str): The ID of the bank unit associated with the alert.

        Returns:
            bool: Returns True if the alert was successfully created, False otherwise.
        """
        # Construct the payload to be sent in the POST request
        payload = {
            "kpi": kpi,
            "data": value,
            "severity": severity,
            "category": category,
            "batteryUnitId": battery_unit_id,
            "bankUnitId": bank_unit_id,
            "assetCode": self.asset_code,  # Include the asset code associated with the alert
            "siteCode": self.site_code,
            "time": datetime.now().isoformat()
        }
        logging.info(f"[Tenant-{tenant_id}] Sending alert creation request to {self.url} : {payload}")
        # Make the POST request to create the alert
        try:
            headers = {"Content-Type": "application/json"}  # Define the headers (specifying JSON content type)
            response = requests.put(self.url, json=payload, headers=headers)  # Send the POST request
            # Handle the response based on the status code
            if response.status_code == 200:  # If the response status is 200 (success)
                logging.info(f"[Tenant-{tenant_id}] Alert created successfully : {response.json()}")  # Log success
                return True  # Return True if the alert was created successfully
            else:  # If the response indicates failure
                logging.error(
                    f"[Tenant-{tenant_id}] Failed to create alert. Status code: {response.status_code} | Response: {response.text}")
                return False  # Return False if alert creation failed
        except requests.RequestException as e:  # Catch any exceptions that occur during the request
            logging.error(f"[Tenant-{tenant_id}] An error occurred while creating the alert: {e}")  # Log the error
            return False  # Return False in case of an error
