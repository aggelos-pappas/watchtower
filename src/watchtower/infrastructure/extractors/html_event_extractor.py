from __future__ import annotations

from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from watchtower.domain.events.entities import Event
from watchtower.domain.watches.entities import Watch
from watchtower.domain.watches.value_objects import build_event_fingerprint, build_source_event_key


class HtmlEventExtractor:
    name = "html"

    def extract(self, watch: Watch, content: str) -> list[Event]:
        soup = BeautifulSoup(content, "html.parser")
        selector = watch.selector or "article.event"
        containers = soup.select(selector)
        events: list[Event] = []
        for item in containers:
            title = self._text(item, "h2") or self._text(item, "[data-title]") or "Untitled event"
            start_value = self._attr(item, "time", "datetime") or self._attr(item, "[data-start]", "datetime")
            end_value = self._attr(item, "time.end", "datetime") or self._attr(item, "[data-end]", "datetime")
            location = self._text(item, ".location") or self._text(item, "[data-location]")
            description = self._text(item, ".description") or self._text(item, "[data-description]")
            starts_at = self._parse_datetime(start_value)
            ends_at = self._parse_datetime(end_value) if end_value else None
            source_key = build_source_event_key(title, starts_at, location, watch.url)
            fingerprint = build_event_fingerprint(title, description, starts_at, ends_at, "UTC", location, watch.url, "active")
            events.append(
                Event(
                    watch_id=watch.id,
                    source_event_key=source_key,
                    title=title,
                    description=description,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    timezone="UTC",
                    location=location,
                    source_url=watch.url,
                    status="active",
                    fingerprint=fingerprint,
                )
            )
        return events

    @staticmethod
    def _text(item: Any, selector: str) -> str | None:
        part = item.select_one(selector)
        if part is None:
            return None
        return part.get_text(" ", strip=True)

    @staticmethod
    def _attr(item: Any, selector: str, attribute: str) -> str | None:
        part = item.select_one(selector)
        if part is None:
            return None
        value = part.get(attribute)
        return value.strip() if isinstance(value, str) else None

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime:
        if value is None:
            raise ValueError("Missing datetime value for event")
        return datetime.fromisoformat(value)
