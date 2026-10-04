from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from watchtower.domain.events.entities import Event
from watchtower.domain.watches.entities import Watch
from watchtower.infrastructure.database.models import EventModel, WatchModel


class InMemoryWatchRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, Watch] = {}

    def add(self, watch: Watch) -> Watch:
        self._items[watch.id] = watch
        return watch

    def get_by_id(self, watch_id: UUID) -> Watch | None:
        return self._items.get(watch_id)

    def list(self) -> list[Watch]:
        return list(self._items.values())

    def update(self, watch: Watch) -> Watch:
        self._items[watch.id] = watch
        return watch

    def delete(self, watch_id: UUID) -> None:
        self._items.pop(watch_id, None)


class InMemoryEventRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, Event] = {}

    def add(self, event: Event) -> Event:
        self._items[event.id] = event
        return event

    def list_by_watch(self, watch_id: UUID) -> list[Event]:
        return [e for e in self._items.values() if e.watch_id == watch_id]

    def get_by_watch_and_key(self, watch_id: UUID, source_event_key: str) -> Event | None:
        for event in self._items.values():
            if event.watch_id == watch_id and event.source_event_key == source_event_key:
                return event
        return None

    def update(self, event: Event) -> Event:
        self._items[event.id] = event
        return event

    def list(self) -> list[Event]:
        return list(self._items.values())

    def mark_missing(self, watch_id: UUID, known_event_keys: set[str]) -> list[Event]:
        updated: list[Event] = []
        for event in self.list_by_watch(watch_id):
            if event.source_event_key not in known_event_keys and event.status != "dismissed":
                event.status = "possibly_removed"
                event.updated_at = datetime.now(timezone.utc)
                updated.append(event)
        return updated
