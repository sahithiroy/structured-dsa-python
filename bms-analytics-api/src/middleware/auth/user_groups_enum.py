from enum import Enum

# Enum class to represent user roles
class UserGroups(str, Enum):
    """
    This Enum class defines the different user roles within the application.
    Each role represents a specific set of permissions or responsibilities.

    Attributes:
    - AccountAdmin: A role that typically has administrative privileges,
      such as managing users, configurations, or access control.
    - AccountUser: A role for regular users with limited permissions,
      such as accessing standard features or data within their account scope.
    """
    AccountAdmin = "AccountAdmin"  # Represents an administrator role for the account
    AccountUser = "AccountUser"  # Represents a standard user role for the account
