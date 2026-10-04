from __future__ import annotations

from watchtower.infrastructure.extractors.html_event_extractor import HtmlEventExtractor


class UnknownExtractorTypeError(ValueError):
    pass


class ExtractorRegistry:
    def __init__(self) -> None:
        self._registry = {
            "html": HtmlEventExtractor,
        }

    def get(self, extraction_type: str):
        provider = self._registry.get(extraction_type)
        if provider is None:
            raise UnknownExtractorTypeError(f"Unknown extractor type: {extraction_type}")
        return provider()
