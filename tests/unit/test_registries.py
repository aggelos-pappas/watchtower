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
