from .base_media import BaseMedia
from PIL import Image

class ImageMedia(BaseMedia):
    def __init__(self, raw_bytes: bytes, image: Image) -> None:
        self.image = image
        super().__init__(raw_bytes)