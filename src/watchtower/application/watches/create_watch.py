from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from watchtower.domain.watches.entities import Watch


class CreateWatch:
    def __init__(self, watch_repository):
        self.watch_repository = watch_repository

    def execute(self, *, name: str, url: str, source_type: str = "http", extraction_type: str = "html", selector: str | None = None, interval_seconds: int = 300, enabled: bool = True) -> Watch:
        watch = Watch(
            id=uuid4(),
            name=name,
            url=url,
            source_type=source_type,
            selector=selector,
            extraction_type=extraction_type,
            interval_seconds=interval_seconds,
            enabled=enabled,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return self.watch_repository.add(watch)
