from __future__ import annotations

from icalendar import Calendar, Event as ICalEvent

from watchtower.domain.events.entities import Event


class IcalendarProvider:
    name = "icalendar"

    def create(self, event: Event, calendar_id: str) -> str:
        return f"ical-{event.id}"

    def update(self, event: Event, external_event_id: str) -> None:
        return None

    def delete(self, external_event_id: str) -> None:
        return None

    def export_ics(self, events: list[Event]) -> str:
        cal = Calendar()
        cal.add("prodid", "-//Watchtower//EN")
        cal.add("version", "2.0")
        for event in events:
            ical_event = ICalEvent()
            ical_event.add("summary", event.title)
            ical_event.add("dtstart", event.starts_at)
            if event.ends_at is not None:
                ical_event.add("dtend", event.ends_at)
            if event.location:
                ical_event.add("location", event.location)
            if event.description:
                ical_event.add("description", event.description)
            cal.add_component(ical_event)
        return cal.to_ical().decode("utf-8")
