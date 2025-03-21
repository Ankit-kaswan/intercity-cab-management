from enum import Enum


class CabState(str, Enum):
    IDLE = "IDLE"
    ON_TRIP = "ON_TRIP"
    MAINTENANCE = "MAINTENANCE"
