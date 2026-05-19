from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class KPIDataPoint(BaseModel):
    time: datetime  # Timestamp of the data point.
    v: float  # Voltage value recorded at this time.
    i: float  # Current value recorded at this time.
    soc: float  # State of charge percentage.
    mode: int  # Operational mode of the system (e.g., 0 for idle, 1 for active, etc.).
    v_as: Optional[int] = None  # Voltage anomaly status, if any (1 for anomalous, 0 for normal).
    ci_as: Optional[int] = None  # Charging current anomaly status, if any.
    di_as: Optional[int] = None  # Discharging current anomaly status, if any.
    soc_as: Optional[int] = None  # State of charge anomaly status, if any.
    e_state: Optional[str] = None  # Error state indicator (e.g., 'E' for error, 'N' for normal).
    overall_as: Optional[int] = None  # Overall anomaly status.

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "time": "2024-12-27T10:15:00Z",
                "v": 3.6,
                "i": 0.5,
                "soc": 80,
                "mode": 1,
                "v_as": 1,
                "ci_as": 0,
                "di_as": 1,
                "soc_as": 0,
                "e_state": "E",
                "overall_as": 1
            }
        }


class KPIPayload(BaseModel):
    now: KPIDataPoint  # Current KPI data point snapshot.
    prev: KPIDataPoint  # Previous KPI data point snapshot.
    asset_code: str  # Unique identifier for the asset generating the data.
    site_code: str  # Code identifying the site where the asset is located.
    bank_unit_id: str  # Identifier for the specific battery bank unit.
    battery_unit_id: str  # Identifier for the individual battery unit.
    tenant_id: str  # Unique identifier for the tenant owning the asset.
    tenant_namespace: str  # Namespace for tenant-specific data segmentation.

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "tenant_id": "tenant_123",
                "tenant_namespace": "vibe_motors",
                "asset_code": "A1",
                "site_code": "S1",
                "battery_unit_id": "B1",
                "bank_unit_id": "Bank1",
                "prev": {
                    "time": "2024-12-27T10:15:00Z",
                    "v": 3.6,
                    "i": 0.5,
                    "soc": 80,
                    "mode": 1,
                    "v_as": 1,
                    "ci_as": 0,
                    "di_as": 1,
                    "soc_as": 0,
                    "e_state": "N",
                    "overall_as": 1
                },
                "now": {
                    "time": "2024-12-27T10:20:00Z",
                    "v": 3.4,
                    "i": 0.7,
                    "soc": 78,
                    "mode": 1,
                    "v_as": 0,
                    "ci_as": 1,
                    "di_as": 0,
                    "soc_as": 1,
                    "e_state": "E",
                    "overall_as": 0
                }
            }
        }


class IncidentAnomaly(BaseModel):
    batteryUnitId: Optional[str] = None  # Id of the problematic battery.
    bankUnitId: str  # Id of the bank in which the problematic battery is present.
    kpi: str  # Name of the KPI that is problematic (e.g., voltage, current).
    severity:int
    values: Optional[list[float]] = None  # The values of the above KPI during the incident duration.
    latestTrend: Optional[str] = None  # Latest behavioral trend observed for the KPI.
    forecast: Optional[list[float]] = None  # Forecasted behavioral trend estimated for the KPI.
    overallTrend: Optional[str] = None  # Overall behavioral trend observed for the KPI.

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "batteryUnitId": "B1",
                "bankUnitId": "Bank1",
                "kpi": "voltage",
                "severity": 1,
                "values": [3.6, 3.5, 3.4],
                "latestTrend": "Decreasing",
                "forecast": [3.2,3.4,3.4],
                "overallTrend": "Fluctuating"
            }
        }


class Incident(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    incidentId: str  # Unique id for the incident (e.g., INC-123456).
    summary: Optional[str] = None  # Natural language summary of the incident.
    startedAt: datetime  # Timestamp at which the incident started.
    stoppedAt: Optional[datetime] = None  # Timestamp at which the incident stopped.
    status: int  # Status of the incident: 0 → ongoing, 1 → under-observation, 2 → closed.
    anomalies: Optional[list[IncidentAnomaly]] = None  # List of anomalous battery + KPI information for this incident.
    assetCode: str  # Id of the asset for which this incident is generated.
    ownerId: str  # Id of the tenant.
    createdAt: datetime  # Timestamp at which the incident is created.
    updatedAt: datetime  # Timestamp at which the incident is last updated.

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "abcd1234efgh5678",
                "incidentId": "INC-20250121-001",
                "summary": "Voltage anomaly detected in battery B1 of bank Bank1.",
                "startedAt": "2025-01-20T14:00:00Z",
                "stoppedAt": None,
                "status": 0,
                "owner_id": "sahithi",
                "anomalies": [
                    {
                        "batteryId": "B1",
                        "bankId": "Bank1",
                        "kpi": "voltage",
                        "severity":1,
                        "values": [3.6, 3.4, 3.2],
                        "latestTrend": "Decreasing",
                        "forecast": "Stable",
                        "overallTrend": "Fluctuating"
                    }
                ],
                "assetCode": "A1",
                "ownerId": "tenant_123",
                "createdAt": "2025-01-20T14:05:00Z",
                "updatedAt": "2025-01-20T14:05:00Z"
            }
        }


# Define a Pydantic model for validation
class IncidentCounterModel(BaseModel):
    owner_id: str
    asset_code: str
    incident: Optional[int] = 1  # Default to 1 if not specified
