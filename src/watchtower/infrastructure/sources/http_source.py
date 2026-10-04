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
