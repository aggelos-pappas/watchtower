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
