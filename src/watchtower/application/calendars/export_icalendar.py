from __future__ import annotations

from watchtower.infrastructure.calendars.icalendar_provider import IcalendarProvider


class ExportICalendar:
    def __init__(self, provider: IcalendarProvider | None = None):
        self.provider = provider or IcalendarProvider()

    def execute(self, events: list) -> str:
        return self.provider.export_ics(events)
