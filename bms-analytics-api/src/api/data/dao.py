import logging
import traceback
from typing import Optional, List
from src.api.database import Database
from src.api.incidents.enums import BatteryKPI, BatteryNames
from datetime import datetime


class IncidentData:
    def __init__(self, tenant_namespace: str, siteCode: str, assetCode: str):
        """
            Initializes the IncidentData class with the provided tenant namespace.
        """

        self.db = Database(tenant_namespace)  # Initialize the database
        self.battery_metrics_collection = self.db.get_collection(f"{siteCode}_{assetCode}_battery_metrics")

    def fetch_battery_metrics_for_given_time_range(self, start_time: datetime, end_time: datetime, kpi: str,
                                                   bank_id: str, battery_id: str) -> Optional[List[float]]:
        """
        Fetch battery metrics for a given time range and KPI.

        :param start_time: Start time of the query range.
        :param end_time: End time of the query range.
        :param kpi: KPI to filter data (e.g., 'current', 'voltage').
        :param bank_id: The bank ID to filter data.
        :param battery_id: The battery ID to filter data.
        :return: List of battery metric records or None if no data found.
        """
        pipeline = [
            {
                "$match": {
                    "attributes.bnkId": bank_id,
                    "attributes.batteryUid": battery_id,
                    "time": {"$gte": start_time, "$lt": end_time}
                }
            },
            {
                "$group": {
                    "_id": {
                        "bnkId": "$attributes.bnkId",
                        "batteryUid": "$attributes.batteryUid",
                        "bin": {
                            "$dateTrunc": {
                                "date": "$time",
                                "unit": "minute",
                                "binSize": self.calculate_step_size(start_time, end_time)
                            }
                        }
                    },
                    "i": {"$avg": "$current"},
                    "di": {
                        "$min": {
                            "$cond": [{"$lt": ["$current", 0]}, "$current", 0]
                        }
                    },
                    "ci": {
                        "$max": {
                            "$cond": [{"$gte": ["$current", 0]}, "$current", 0]
                        }
                    },
                    "v": {"$avg": "$voltage"},
                    "soc": {"$max": "$soc"},
                    "sos": {"$min": "$sos"}
                }
            },
            {
                "$sort": {"_id.bin": 1}
            },
            {
                "$project": {
                    "_id": 0,
                    "ts": "$_id.bin",
                    "bankid": "$_id.bnkId",
                    "batteryid": "$_id.batteryUid",
                    "v": {"$round": ["$v", 2]},
                    "i": {"$round": ["$i", 2]},
                    "di": {"$round": ["$di", 2]},
                    "ci": {"$round": ["$ci", 2]},
                    "soc": {"$round": ["$soc", 0]}
                }
            }
        ]
        try:
            result = list(self.battery_metrics_collection.aggregate(pipeline))
            if not result:
                return None

            if kpi == BatteryKPI.VOLTAGE.value:
                # Extract the values of "v"
                return [record["v"] for record in result if "v" in record]
            elif kpi == BatteryKPI.CURRENT.value:
                if battery_id == BatteryNames.BATTERIES.value:
                    return [record["ci"] for record in result if "ci" in record]
                else:
                    return [record["di"] for record in result if "di" in record]

            elif kpi == BatteryKPI.STATE_OF_CHARGE.value:
                # Return "soc" values
                return [record["soc"] for record in result if "soc" in record]
            else:
                logging.warning(f"Unsupported KPI: {kpi}")
                return None

        except Exception as e:
            logging.error(f"Error fetching battery metrics: {e}")
            logging.error(traceback.format_exc())
            return None

    def fetch_latest_battery_metrics_after_given_time(self, start_time: datetime, kpi: str) -> Optional[List[float]]:
        """
        Fetches battery metrics data for a given time range.

        Parameters:
        - start_time: The start time to filter data.
        - kpi: The key performance indicator (KPI) to fetch data for ('v', 'i', or 'soc').

        Returns:
        - A list of values corresponding to the requested KPI (voltage, current, or state of charge).
          Returns None if an invalid KPI is provided.
        """
        latest_records_count = 50
        try:
            # Check if the KPI is 'v' for voltage
            if kpi == BatteryKPI.VOLTAGE.value:
                query = {
                    "time": {"$gte": start_time},  # Filter data after the start_time
                    "anm.v_as": {"$gt": 0}  # Filter documents where 'v_as' > 0
                }

                # Fetch matching data from the MongoDB collection
                data = list(
                    self.battery_metrics_collection.find(query)
                    .sort("time", -1)  # Sort by 'time' in descending order
                    .limit(latest_records_count)  # Limit to 50 records
                )

                # Extract the voltage values where 'v_as' > 0
                voltage_values = [record['voltage'] for record in data if record.get('anm', {}).get('v_as', 0) > 0]

                return voltage_values

            # Check if the KPI is 'i' for current
            elif kpi == BatteryKPI.CURRENT.value:
                query = {
                    "time": {"$gte": start_time},  # Filter data after the start_time
                    "$or": [
                        {"anm.ci_as": {"$gt": 0}},  # Filter documents where 'ci_as' > 0
                        {"anm.di_as": {"$gt": 0}}  # Filter documents where 'di_as' > 0
                    ],
                }

                # Fetch matching data from the MongoDB collection
                data = list(
                    self.battery_metrics_collection.find(query)
                    .sort("time", -1)  # Sort by 'time' in descending order
                    .limit(latest_records_count)  # Limit to 50 records
                )

                # Extract the current values where 'ci_as' > 0 or 'di_as' > 0
                current_values = [record['current'] for record in data if
                                  record.get('anm', {}).get('ci_as', 0) > 0 or record.get('anm', {}).get('di_as',
                                                                                                         0) > 0]

                # Return the extracted current values
                return current_values

            # Check if the KPI is 'soc' for state of charge
            elif kpi == BatteryKPI.STATE_OF_CHARGE.value:
                query = {
                    "time": {"$gte": start_time},  # Filter data after the start_time
                    "anm.soc_as": {"$gt": 0}  # Filter documents where 'soc_as' > 0
                }

                # Fetch matching data from the MongoDB collection
                data = list(
                    self.battery_metrics_collection.find(query)
                    .sort("time", -1)  # Sort by 'time' in descending order
                    .limit(latest_records_count)  # Limit to 50 records
                )

                # Extract the state of charge values where 'soc_as' > 0
                soc_values = [record['soc'] for record in data if record.get('anm', {}).get('soc_as', 0) > 0]

                return soc_values

            # If an invalid KPI is provided
            else:
                logging.info("Invalid KPI provided. Returning None.")
                return None

        # Catch any exceptions and log them
        except Exception as e:
            logging.error(f"Error fetching battery metrics: {traceback.format_exc()}")
            return []

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
                {
                    "$sort": {
                        "time": -1
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "batteryUid": "$attributes.batteryUid"
                        },
                        "latestEntry": {
                            "$first": "$$ROOT"
                        }
                    }
                },
                {
                    "$replaceRoot": {
                        "newRoot": "$latestEntry"
                    }
                },
                {
                    "$match": {
                        "attributes.bnkId": "Bank_1"
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "voltage": {
                            "$sum": "$voltage"
                        }
                    }
                }
            ]

            # Execute the aggregation query
            result = list(self.battery_metrics_collection.aggregate(
                pipeline,
                maxTimeMS=60000,
                allowDiskUse=True
            ))
            if len(result) > 0:
                return result[0].get('voltage')
            # If no result is found, return None or raise an exception
            return None

        except Exception as e:
            # Log the error and re-raise the exception
            print(f"Error reading bank voltage: {e}")
            return None

    def calculate_step_size(self, from_date: datetime, to_date: datetime):
        duration_in_seconds = abs((to_date - from_date).total_seconds())
        duration_in_minutes = duration_in_seconds / 60
        duration_in_hours = duration_in_minutes / 60
        duration_in_days = duration_in_hours / 24
        diff_in_weeks = duration_in_days / 7
        diff_in_months = duration_in_days / 30
        diff_in_years = duration_in_days / 365

        if duration_in_hours <= 1:
            return 5
        elif duration_in_hours <= 3:
            return 15
        elif duration_in_hours <= 6:
            return 30
        elif duration_in_hours <= 12:
            return 60
        elif duration_in_hours <= 24:
            return 120
        elif 1 < duration_in_days <= 3:
            return 360
        elif 3 < duration_in_days <= 5:
            return 720
        elif 5 < duration_in_days <= 15:
            return 1440
        elif 15 < duration_in_days <= 30:
            return 2880
        elif 1 < diff_in_months <= 3:
            return 8640
        elif 3 < diff_in_months <= 6:
            return 21600
        elif diff_in_years == 1:
            return 43200
        else:
            return "step Size : "
