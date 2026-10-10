"""Cached response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class Cached(Envelope):
    """Response decorator attaching the Cache-Control HTTP header in Pure OOP."""

    def __init__(self, origin: Response, max_age: int = 3600, directive: str = "public") -> None:
        super().__init__(origin)
        self._max_age = max_age
        self._directive = directive

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        val = f"{self._directive}, max-age={self._max_age}" if self._max_age >= 0 else self._directive
        headers = list(origin_head.headers())
        headers.append((b"Cache-Control", val.encode("latin1")))
        return Head(status=origin_head.status(), headers=headers)


class NoCache(Envelope):
    """Response decorator disabling caching via Cache-Control: no-cache."""

    def __init__(self, origin: Response) -> None:
        super().__init__(Cached(origin, max_age=-1, directive="no-cache"))
