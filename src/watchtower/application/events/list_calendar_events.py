from __future__ import annotations

from datetime import datetime


class ListCalendarEvents:
    def __init__(self, event_repository):
        self.event_repository = event_repository

    def execute(self, *, watch_id=None, from_date: datetime | None = None, to_date: datetime | None = None):
        events = self.event_repository.list() if watch_id is None else self.event_repository.list_by_watch(watch_id)
        results = []
        for event in events:
            if from_date and event.starts_at < from_date:
                continue
            if to_date and event.starts_at > to_date:
                continue
            results.append(event)
        return results
