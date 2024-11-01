from enum import Enum


class SessionStatus(Enum):
    Active = 'Active'
    Expired = 'Expired'
    Locked_out = 'Locked_out'
    Invalid = "Invalid"

