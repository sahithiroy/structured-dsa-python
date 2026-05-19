from typing import Optional
from database import Database


class IncidentData:
    def __init__(self, tenant_namespace: str, siteCode: str, assetCode: str):
        """
        Initializes the IncidentData class with the provided tenant namespace.
        """

        # self.db = Database(tenant_namespace)  # Initialize the database
        self.tenant_namespace = tenant_namespace
        self.siteCode = siteCode
        self.assetCode = assetCode

    def read_bank_voltage(self) -> Optional[float]:
        """
        Reads the latest voltage value for a specific bank unit.

        Args:
            owner_id: ID of the owner.
            asset_code: Code of the asset.
            bank_unit_id: ID of the bank unit.
            site_code: Code of the site.

        Returns:
            float: The average voltage value for the first 24 documents of the specified bank unit.

        Raises:
            Exception: If there is an error during the database operation.
        """
        try:

            pipeline = [
                {"$sort": {"time": -1}},
                {
                    "$group": {
                        "_id": {"batteryUid": "$attributes.batteryUid"},
                        "latestEntry": {"$first": "$$ROOT"},
                    }
                },
                {"$replaceRoot": {"newRoot": "$latestEntry"}},
                {"$match": {"attributes.bnkId": "Bank_1"}},
                {"$group": {"_id": None, "voltage": {"$sum": "$voltage"}}},
            ]
            with Database(self.tenant_namespace) as db:
                result = list(
                    db.get_collection(
                        f"{self.siteCode}_{self.assetCode}_battery_metrics"
                    ).aggregate(pipeline, maxTimeMS=60000, allowDiskUse=True)
                )
            if len(result) > 0:
                return round(result[0].get("voltage", 0), 2)
            # If no result is found, return None or raise an exception
            return None

        except Exception as e:
            # Log the error and re-raise the exception
            print(f"Error reading bank voltage: {e}")
            return None
