from __future__ import annotations

from watchtower.infrastructure.sources.http_source import HttpSource
from watchtower.infrastructure.sources.playwright_source import PlaywrightSource


class UnknownSourceTypeError(ValueError):
    pass


class SourceRegistry:
    def __init__(self) -> None:
        self._registry = {
            "http": HttpSource,
            "playwright": PlaywrightSource,
        }

    def get(self, source_type: str):
        provider = self._registry.get(source_type)
        if provider is None:
            raise UnknownSourceTypeError(f"Unknown source type: {source_type}")
        return provider()
