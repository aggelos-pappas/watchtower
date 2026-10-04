from __future__ import annotations

from datetime import datetime
from hashlib import sha256


def normalize_text(value: str | None) -> str:
    return (value or "").strip().lower()


def build_source_event_key(title: str, starts_at: datetime, location: str | None, source_url: str) -> str:
    payload = "|".join([
        normalize_text(title),
        starts_at.astimezone().isoformat(),
        normalize_text(location),
        normalize_text(source_url),
    ])
    return f"sha256:{sha256(payload.encode('utf-8')).hexdigest()}"


def build_event_fingerprint(title: str, description: str | None, starts_at: datetime, ends_at: datetime | None, timezone: str, location: str | None, source_url: str, status: str) -> str:
    payload = "|".join([
        normalize_text(title),
        normalize_text(description),
        starts_at.astimezone().isoformat(),
        (ends_at.astimezone().isoformat() if ends_at else ""),
        normalize_text(timezone),
        normalize_text(location),
        normalize_text(source_url),
        normalize_text(status),
    ])
    return f"sha256:{sha256(payload.encode('utf-8')).hexdigest()}"
