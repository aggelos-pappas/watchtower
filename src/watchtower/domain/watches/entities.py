from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(slots=True)
class Watch:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    url: str = ""
    source_type: str = "http"
    selector: str | None = None
    extraction_type: str = "html"
    interval_seconds: int = 300
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
