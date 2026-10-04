from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(slots=True)
class Event:
    id: UUID = field(default_factory=uuid4)
    watch_id: UUID | None = None
    source_event_key: str = ""
    title: str = ""
    description: str | None = None
    starts_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ends_at: datetime | None = None
    timezone: str = "UTC"
    location: str | None = None
    source_url: str = ""
    status: str = "active"
    fingerprint: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
