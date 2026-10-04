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
    watch = Watch(id=uuid4(), name="Example", url="https://example.com", source_type="fake", extraction_type="html")
    repo.add(watch)
    source_registry = SourceRegistry()
    source_registry._registry["fake"] = lambda: FakeSource()
    run_service = RunWatch(repo, event_repo, source_registry, ExtractorRegistry())
    result = run_service.execute(watch.id)
    assert result["event_count"] == 1
