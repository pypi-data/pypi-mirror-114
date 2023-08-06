from .base_enrichment import BaseEnrichment


class TextSentimentEnrichment(BaseEnrichment):
    def __init__(self, sentiment) -> None:
        self.sentiment = sentiment
        super().__init__()
