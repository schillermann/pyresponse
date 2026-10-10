"""Strict-Transport-Security (HSTS) response security decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class Hsts(Envelope):
    """Response decorator setting Strict-Transport-Security header in Pure OOP."""

    def __init__(
        self,
        origin: Response,
        max_age: int = 31536000,
        include_subdomains: bool = True,
        preload: bool = False,
    ) -> None:
        super().__init__(origin)
        self._max_age = max_age
        self._include_subdomains = include_subdomains
        self._preload = preload

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        parts = [f"max-age={self._max_age}"]
        if self._include_subdomains:
            parts.append("includeSubDomains")
        if self._preload:
            parts.append("preload")
        headers = list(origin_head.headers())
        headers.append((b"Strict-Transport-Security", "; ".join(parts).encode("latin1")))
        return Head(status=origin_head.status(), headers=headers)
