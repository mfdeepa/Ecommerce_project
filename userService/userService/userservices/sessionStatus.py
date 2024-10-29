from enum import Enum


class SessionStatus(Enum):
    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    LOGGED_OUT = 'LOGGED_OUT'
    INVALID = 'INVALID'
