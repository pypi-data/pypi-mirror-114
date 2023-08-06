from abc import ABC
from datetime import datetime


class BaseEntry(ABC):
    def __init__(self, profile: str, timestamp: datetime) -> None:
        self.profile = profile
        self.timestamp = timestamp
        super().__init__()
