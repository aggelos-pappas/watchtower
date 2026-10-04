from __future__ import annotations

from watchtower.domain.watches.entities import Watch


class PlaywrightSource:
    name = "playwright"

    def fetch(self, watch: Watch) -> str:
        raise NotImplementedError("PlaywrightSource is scaffolded and will be implemented later.")
