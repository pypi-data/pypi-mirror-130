from enum import Enum


class PropertiesCalculationType(int, Enum):
    TP = 0
    "0 - Fixed Temperature/Pressure"
    TV = 1
    "1 - Fixed Temperature/Volume"
    PV = 2
    """2 - Fixed Pressure/Volume"""

    def __str__(self) -> str:
        return str(self.value)
