from enum import Enum


# Enum class to represent user roles
class UserGroups(str, Enum):
    AccountAdmin = "AccountAdmin"
    AccountUser = "AccountUser"
