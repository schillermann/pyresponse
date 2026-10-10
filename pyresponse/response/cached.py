"""Cached response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Cached(Envelope):
    """Response decorator attaching the Cache-Control HTTP header."""

    def __init__(self, origin: Response, max_age: int = 3600, directive: str = "public") -> None:
        val = f"{directive}, max-age={max_age}" if max_age >= 0 else directive
        super().__init__(Header(origin, "Cache-Control", val))


class NoCache(Envelope):
    """Response decorator disabling caching via Cache-Control: no-cache."""

    def __init__(self, origin: Response) -> None:
        super().__init__(Cached(origin, max_age=-1, directive="no-cache"))
