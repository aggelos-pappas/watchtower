from datetime import datetime, timezone

from watchtower.domain.watches.value_objects import build_source_event_key


def test_source_event_key_is_deterministic() -> None:
    start = datetime(2027, 1, 12, 8, 0, tzinfo=timezone.utc)
    first = build_source_event_key("Exam", start, "Room A", "https://example.com")
    second = build_source_event_key("Exam", start, "Room A", "https://example.com")
    assert first == second
