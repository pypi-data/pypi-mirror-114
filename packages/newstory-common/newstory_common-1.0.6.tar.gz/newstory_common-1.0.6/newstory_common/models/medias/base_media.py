from abc import ABC

class BaseMedia(ABC):
    def __init__(self, raw_bytes:bytes) -> None:
        self.raw_bytes=raw_bytes
        super().__init__()