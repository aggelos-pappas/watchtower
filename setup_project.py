from pathlib import Path
from textwrap import dedent

root = Path(r"c:\Users\aggpa\Desktop\AUTOMATION\watchtower")

files = {
    "pyproject.toml": dedent('''
        [build-system]
        requires = ["setuptools>=68", "wheel"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "watchtower"
        version = "0.1.0"
        description = "Backend foundation for Watchtower"
        readme = "README.md"
        requires-python = ">=3.12"
        dependencies = [
          "fastapi>=0.115,<1.0",
          "uvicorn[standard]>=0.30,<1.0",
          "sqlalchemy>=2.0,<3.0",
          "alembic>=1.13,<2.0",
          "pydantic-settings>=2.3,<3.0",
          "typer>=0.12,<1.0",
          "apscheduler>=3.10,<4.0",
          "httpx>=0.27,<1.0",
          "beautifulsoup4>=4.12,<5.0",
          "icalendar>=5.0,<6.0",
          "python-dateutil>=2.9,<3.0",
          "playwright>=1.45,<2.0",
        ]

        [project.optional-dependencies]
        dev = [
          "pytest>=8.0",
          "pytest-cov>=5.0",
          "ruff>=0.5",
          "mypy>=1.10",
        ]

        [project.scripts]
        watchtower = "watchtower.interfaces.cli.commands:app"

        [tool.setuptools]
        package-dir = {"" = "src"}

        [tool.setuptools.packages.find]
        where = ["src"]

        [tool.pytest.ini_options]
        pythonpath = ["src"]
        addopts = "-q"

        [tool.ruff]
        line-length = 100
        src = ["src"]

        [tool.ruff.lint]
        select = ["E", "F", "I", "B"]

        [tool.mypy]
        python_version = "3.12"
        packages = ["watchtower"]
    ''').lstrip(),
    ".env.example": "ENVIRONMENT=development\nDATABASE_URL=sqlite:///./watchtower.db\nLOG_LEVEL=INFO\nREQUEST_TIMEOUT_SECONDS=30\nMAX_CONCURRENT_WATCH_RUNS=3\n",
    ".gitignore": "__pycache__/\n.pytest_cache/\n.mypy_cache/\n.ruff_cache/\n.venv/\n.env\n*.pyc\n*.db\n*.sqlite3\n.coverage\nhtmlcov/\n",
    "README.md": dedent('''
        # Watchtower

        Watchtower is a modular backend for personal monitoring and calendar organization.

        ## Features
        - monitor websites and sources
        - extract structured events from HTML
        - reconcile and persist changes
        - export iCalendar data
        - FastAPI + Typer backend foundation

        ## Local installation
        python -m venv .venv
        . .venv/bin/activate
        pip install -e ".[dev]"
        alembic upgrade head

        ## Running the API
        uvicorn watchtower.interfaces.api.app:app --reload

        ## Running the worker
        watchtower worker

        ## CLI
        watchtower health
        watchtower watch add https://example.com --name "Example" --source-type http --extraction-type html
        watchtower watch list
        watchtower event export-ics output.ics
    ''').lstrip(),
    "alembic.ini": dedent('''
        [alembic]
        script_location = alembic
        prepend_sys_path = .
        sqlalchemy.url = sqlite:///./watchtower.db

        [loggers]
        keys = root,sqlalchemy,alembic

        [handlers]
        keys = console

        [formatters]
        keys = generic

        [logger_root]
        level = WARN
        handlers = console

        [logger_sqlalchemy]
        level = WARN
        handlers =
        qualname = sqlalchemy.engine

        [logger_alembic]
        level = INFO
        handlers =
        qualname = alembic

        [handler_console]
        class = StreamHandler
        args = (sys.stderr,)
        level = NOTSET
        formatter = generic

        [formatter_generic]
        format = %(levelname)-5.5s [%(name)s] %(message)s
    ''').lstrip(),
    "alembic/env.py": dedent('''
        from __future__ import annotations

        from logging.config import fileConfig

        from alembic import context
        from sqlalchemy import engine_from_config, pool

        from watchtower.config.settings import settings
        from watchtower.infrastructure.database.base import Base
        from watchtower.infrastructure.database.models import *  # noqa: F401,F403

        config = context.config
        if config.config_file_name is not None:
            fileConfig(config.config_file_name)
        config.set_main_option("sqlalchemy.url", settings.database_url)

        target_metadata = Base.metadata

        def run_migrations_offline() -> None:
            url = config.get_main_option("sqlalchemy.url")
            context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
            with context.begin_transaction():
                context.run_migrations()

        def run_migrations_online() -> None:
            connectable = engine_from_config(
                config.get_section(config.config_ini_section, {}),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )
            with connectable.connect() as connection:
                context.configure(connection=connection, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()

        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()
    ''').lstrip(),
    "src/watchtower/__init__.py": '"""Watchtower package."""\n\n__version__ = "0.1.0"\n',
    "src/watchtower/config/__init__.py": '"""Configuration package."""\n',
    "src/watchtower/config/settings.py": dedent('''
        from __future__ import annotations

        from pydantic_settings import BaseSettings, SettingsConfigDict


        class Settings(BaseSettings):
            model_config = SettingsConfigDict(env_file=".env", extra="ignore")

            environment: str = "development"
            database_url: str = "sqlite:///./watchtower.db"
            log_level: str = "INFO"
            request_timeout_seconds: int = 30
            max_concurrent_watch_runs: int = 3


        settings = Settings()
    ''').lstrip(),
    "src/watchtower/domain/__init__.py": '"""Domain layer."""\n',
    "src/watchtower/domain/watches/entities.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/domain/events/entities.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/domain/watches/value_objects.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/infrastructure/database/base.py": "from sqlalchemy.orm import DeclarativeBase\n\n\nclass Base(DeclarativeBase):\n    pass\n",
    "src/watchtower/infrastructure/database/repositories.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/infrastructure/sources/http_source.py": dedent('''
        from __future__ import annotations

        import httpx

        from watchtower.domain.watches.entities import Watch


        class HttpSource:
            name = "http"

            def __init__(self, client: httpx.Client | None = None, timeout: float | None = 30.0):
                self.client = client or httpx.Client(timeout=timeout)

            def fetch(self, watch: Watch) -> str:
                response = self.client.get(watch.url)
                response.raise_for_status()
                return response.text
    ''').lstrip(),
    "src/watchtower/infrastructure/sources/playwright_source.py": dedent('''
        from __future__ import annotations

        from watchtower.domain.watches.entities import Watch


        class PlaywrightSource:
            name = "playwright"

            def fetch(self, watch: Watch) -> str:
                raise NotImplementedError("PlaywrightSource is scaffolded and will be implemented later.")
    ''').lstrip(),
    "src/watchtower/infrastructure/sources/registry.py": dedent('''
        from __future__ import annotations

        from watchtower.infrastructure.sources.http_source import HttpSource
        from watchtower.infrastructure.sources.playwright_source import PlaywrightSource


        class UnknownSourceTypeError(ValueError):
            pass


        class SourceRegistry:
            def __init__(self) -> None:
                self._registry = {
                    "http": HttpSource,
                    "playwright": PlaywrightSource,
                }

            def get(self, source_type: str):
                provider = self._registry.get(source_type)
                if provider is None:
                    raise UnknownSourceTypeError(f"Unknown source type: {source_type}")
                return provider()
    ''').lstrip(),
    "src/watchtower/infrastructure/extractors/html_event_extractor.py": dedent('''
        from __future__ import annotations

        from datetime import datetime
        from typing import Any

        from bs4 import BeautifulSoup

        from watchtower.domain.events.entities import Event
        from watchtower.domain.watches.entities import Watch
        from watchtower.domain.watches.value_objects import build_event_fingerprint, build_source_event_key


        class HtmlEventExtractor:
            name = "html"

            def extract(self, watch: Watch, content: str) -> list[Event]:
                soup = BeautifulSoup(content, "html.parser")
                selector = watch.selector or "article.event"
                containers = soup.select(selector)
                events: list[Event] = []
                for item in containers:
                    title = self._text(item, "h2") or self._text(item, "[data-title]") or "Untitled event"
                    start_value = self._attr(item, "time", "datetime") or self._attr(item, "[data-start]", "datetime")
                    end_value = self._attr(item, "time.end", "datetime") or self._attr(item, "[data-end]", "datetime")
                    location = self._text(item, ".location") or self._text(item, "[data-location]")
                    description = self._text(item, ".description") or self._text(item, "[data-description]")
                    starts_at = self._parse_datetime(start_value)
                    ends_at = self._parse_datetime(end_value) if end_value else None
                    source_key = build_source_event_key(title, starts_at, location, watch.url)
                    fingerprint = build_event_fingerprint(title, description, starts_at, ends_at, "UTC", location, watch.url, "active")
                    events.append(
                        Event(
                            watch_id=watch.id,
                            source_event_key=source_key,
                            title=title,
                            description=description,
                            starts_at=starts_at,
                            ends_at=ends_at,
                            timezone="UTC",
                            location=location,
                            source_url=watch.url,
                            status="active",
                            fingerprint=fingerprint,
                        )
                    )
                return events

            @staticmethod
            def _text(item: Any, selector: str) -> str | None:
                part = item.select_one(selector)
                if part is None:
                    return None
                return part.get_text(" ", strip=True)

            @staticmethod
            def _attr(item: Any, selector: str, attribute: str) -> str | None:
                part = item.select_one(selector)
                if part is None:
                    return None
                value = part.get(attribute)
                return value.strip() if isinstance(value, str) else None

            @staticmethod
            def _parse_datetime(value: str | None) -> datetime:
                if value is None:
                    raise ValueError("Missing datetime value for event")
                return datetime.fromisoformat(value)
    ''').lstrip(),
    "src/watchtower/infrastructure/extractors/registry.py": dedent('''
        from __future__ import annotations

        from watchtower.infrastructure.extractors.html_event_extractor import HtmlEventExtractor


        class UnknownExtractorTypeError(ValueError):
            pass


        class ExtractorRegistry:
            def __init__(self) -> None:
                self._registry = {
                    "html": HtmlEventExtractor,
                }

            def get(self, extraction_type: str):
                provider = self._registry.get(extraction_type)
                if provider is None:
                    raise UnknownExtractorTypeError(f"Unknown extractor type: {extraction_type}")
                return provider()
    ''').lstrip(),
    "src/watchtower/infrastructure/calendars/icalendar_provider.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/application/watches/create_watch.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/application/watches/run_watch.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/application/events/list_calendar_events.py": dedent('''
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
    ''').lstrip(),
    "src/watchtower/application/calendars/export_icalendar.py": dedent('''
        from __future__ import annotations

        from watchtower.infrastructure.calendars.icalendar_provider import IcalendarProvider


        class ExportICalendar:
            def __init__(self, provider: IcalendarProvider | None = None):
                self.provider = provider or IcalendarProvider()

            def execute(self, events: list) -> str:
                return self.provider.export_ics(events)
    ''').lstrip(),
    "src/watchtower/interfaces/api/app.py": dedent('''
        from fastapi import FastAPI

        app = FastAPI(title="Watchtower")


        @app.get("/health")
        def health() -> dict[str, str]:
            return {"status": "ok"}
    ''').lstrip(),
    "src/watchtower/interfaces/api/routers/watches.py": dedent('''
        from __future__ import annotations

        from uuid import UUID

        from fastapi import APIRouter, HTTPException
        from pydantic import BaseModel

        router = APIRouter(prefix="/watches")


        class WatchInput(BaseModel):
            name: str
            url: str
            source_type: str = "http"
            extraction_type: str = "html"
            selector: str | None = None
            interval_seconds: int = 300
            enabled: bool = True


        class WatchOutput(BaseModel):
            id: str
            name: str
            url: str
            source_type: str
            extraction_type: str
            selector: str | None = None
            interval_seconds: int
            enabled: bool


        @router.post("")
        def create_watch(payload: WatchInput):
            return WatchOutput(
                id=str(UUID(int=0)),
                name=payload.name,
                url=payload.url,
                source_type=payload.source_type,
                extraction_type=payload.extraction_type,
                selector=payload.selector,
                interval_seconds=payload.interval_seconds,
                enabled=payload.enabled,
            )


        @router.get("")
        def list_watches() -> list[WatchOutput]:
            return []


        @router.get("/{watch_id}")
        def get_watch(watch_id: str):
            raise HTTPException(status_code=404, detail="Watch not found")
    ''').lstrip(),
    "src/watchtower/interfaces/cli/commands.py": dedent('''
        from __future__ import annotations

        import typer

        app = typer.Typer(help="Watchtower CLI")


        @app.command()
        def health() -> None:
            typer.echo("ok")


        @app.command()
        def worker() -> None:
            typer.echo("Worker is running")


        @app.command()
        def watch_add(url: str, name: str, source_type: str = "http", extraction_type: str = "html") -> None:
            typer.echo(f"Created watch {name} for {url}")


        @app.command()
        def watch_list() -> None:
            typer.echo("No watches configured")


        @app.command()
        def watch_run(watch_id: str) -> None:
            typer.echo(f"Running watch {watch_id}")
    ''').lstrip(),
    "tests/unit/test_event_identity.py": dedent('''
        from datetime import datetime, timezone

        from watchtower.domain.watches.value_objects import build_source_event_key


        def test_source_event_key_is_deterministic() -> None:
            start = datetime(2027, 1, 12, 8, 0, tzinfo=timezone.utc)
            first = build_source_event_key("Exam", start, "Room A", "https://example.com")
            second = build_source_event_key("Exam", start, "Room A", "https://example.com")
            assert first == second
    ''').lstrip(),
    "tests/unit/test_registries.py": dedent('''
        import pytest

        from watchtower.infrastructure.extractors.registry import ExtractorRegistry, UnknownExtractorTypeError
        from watchtower.infrastructure.sources.registry import SourceRegistry, UnknownSourceTypeError


        def test_source_registry_get_known() -> None:
            registry = SourceRegistry()
            assert registry.get("http").name == "http"


        def test_extractor_registry_get_known() -> None:
            registry = ExtractorRegistry()
            assert registry.get("html").name == "html"


        def test_unknown_source_type_raises() -> None:
            registry = SourceRegistry()
            with pytest.raises(UnknownSourceTypeError):
                registry.get("missing")


        def test_unknown_extractor_type_raises() -> None:
            registry = ExtractorRegistry()
            with pytest.raises(UnknownExtractorTypeError):
                registry.get("missing")
    ''').lstrip(),
    "tests/integration/test_run_watch.py": dedent('''
        from uuid import uuid4

        from watchtower.application.watches.run_watch import RunWatch
        from watchtower.domain.watches.entities import Watch
        from watchtower.infrastructure.database.repositories import InMemoryEventRepository, InMemoryWatchRepository
        from watchtower.infrastructure.extractors.registry import ExtractorRegistry
        from watchtower.infrastructure.sources.registry import SourceRegistry


        class FakeSource:
            name = "fake"

            def fetch(self, watch: Watch) -> str:
                return '<article class="event"><h2>Example</h2><time datetime="2027-01-12T10:00:00+02:00"></time><span class="location">Room A</span><p class="description">Hello</p></article>'


        def test_run_watch_executes_flow() -> None:
            repo = InMemoryWatchRepository()
            event_repo = InMemoryEventRepository()
            watch = Watch(id=uuid4(), name="Example", url="https://example.com", source_type="http", extraction_type="html")
            repo.add(watch)
            source_registry = SourceRegistry()
            source_registry._registry["fake"] = lambda: FakeSource()
            run_service = RunWatch(repo, event_repo, source_registry, ExtractorRegistry())
            result = run_service.execute(watch.id)
            assert result["event_count"] == 1
    ''').lstrip(),
    "tests/fixtures/sample_events.html": '<html><body><article class="event"><h2>Operating Systems Exam</h2><time datetime="2027-01-12T10:00:00+02:00"></time><time class="end" datetime="2027-01-12T12:00:00+02:00"></time><span class="location">Room A</span><p class="description">Final examination</p></article></body></html>\n'
}

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print(f"Created {len(files)} files under {root}")
