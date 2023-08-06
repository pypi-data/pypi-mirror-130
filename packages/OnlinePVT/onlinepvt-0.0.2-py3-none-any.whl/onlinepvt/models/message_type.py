from enum import Enum


class MessageType(int, Enum):
    MESSAGE = 0
    """0 - Message"""
    EXCEPTION = 1
    """1 - Exception"""

    def __str__(self) -> str:
        return str(self.value)
