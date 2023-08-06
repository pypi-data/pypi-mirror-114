from datetime import datetime
from .base_media import BaseMedia
from .base_entry import BaseEntry
from typing import List

class PostEntry(BaseEntry):
    def __init__(self, profile: str, timestamp: datetime, text: str, medias: List[BaseMedia], tags: List[str]) -> None:
        self.text=text
        self.medias=medias
        self.tags=tags
        super().__init__(profile, timestamp)