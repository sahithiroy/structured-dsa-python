from enum import Enum  # Imports the Enum class from the enum module to define enumerations


# Enum class to represent the different types of battery KPIs (Key Performance Indicators)
class BatteryKPI(Enum):
    VOLTAGE = "v"  # Represents the 'Voltage' KPI, assigned the shorthand value "v"
    CURRENT = "i"  # Represents the 'Current' KPI, assigned the shorthand value "i"
    STATE_OF_CHARGE = "soc"  # Represents the 'State of Charge' KPI, assigned the shorthand value "soc"


# Enum class to represent the different statuses of an incident
class IncidentStatus(Enum):
    ONGOING = 0  # Represents an 'Ongoing' incident, assigned the status code 0
    IN_OBSERVATION = 1  # Represents an incident 'In Observation', assigned the status code 1


class AlertCategory(Enum):
    BATTERY = 1
    BANK = 2
    ASSET = 3
    SITE = 4


class ForecastSteps(Enum):
    TWENTY = 20
    THIRTY = 30
    FORTY = 40
    FIFTY = 50


class BatteryNames(Enum):
    BATTERIES = "All Batteries"
