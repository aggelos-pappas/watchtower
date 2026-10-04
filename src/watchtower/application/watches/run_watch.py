from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from watchtower.domain.events.entities import Event


class RunWatch:
    def __init__(self, watch_repository, event_repository, source_registry, extractor_registry, notifier=None):
        self.watch_repository = watch_repository
        self.event_repository = event_repository
        self.source_registry = source_registry
        self.extractor_registry = extractor_registry
        self.notifier = notifier

    def execute(self, watch_id: UUID) -> dict[str, object]:
        watch = self.watch_repository.get_by_id(watch_id)
        if watch is None:
            raise ValueError(f"Watch {watch_id} not found")

        source = self.source_registry.get(watch.source_type)
        content = source.fetch(watch)
        extractor = self.extractor_registry.get(watch.extraction_type)
        events = extractor.extract(watch, content)

        existing = {event.source_event_key: event for event in self.event_repository.list_by_watch(watch_id)}
        inserted: list[Event] = []
        updated: list[Event] = []
        seen: set[str] = set()

        for event in events:
            seen.add(event.source_event_key)
            current = existing.get(event.source_event_key)
            if current is None:
                event.created_at = datetime.now(timezone.utc)
                event.updated_at = datetime.now(timezone.utc)
                inserted.append(self.event_repository.add(event))
            elif current.fingerprint != event.fingerprint:
                event.id = current.id
                event.created_at = current.created_at
                event.updated_at = datetime.now(timezone.utc)
                updated.append(self.event_repository.update(event))

        self.event_repository.mark_missing(watch_id, seen)

        if self.notifier is not None and (inserted or updated):
            self.notifier.notify(f"[{watch.name}] {len(inserted)} new, {len(updated)} updated")

        return {
            "watch_id": str(watch.id),
            "inserted": inserted,
            "updated": updated,
            "event_count": len(events),
            "content_length": len(content),
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
