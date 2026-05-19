from enum import Enum

# Enum class to represent user roles
class Role(str, Enum):
    admin = "Admin"
    user = "User"