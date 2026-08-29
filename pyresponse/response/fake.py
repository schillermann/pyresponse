"""Fake HTTP Response implementation for testing."""

from typing import AsyncIterator
from pyresponse.response.response import Head, Response


class Fake(Response):
    """Fake HTTP Response for testing and simulation."""

    def __init__(
        self,
        status: int = 200,
        headers: list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...] = (),
        body_bytes: bytes = b"",
    ) -> None:
        self._status = status
        self._headers = headers
        self._body_bytes = body_bytes

    async def head(self) -> Head:
        return Head(status=self._status, headers=self._headers)

    async def body(self) -> AsyncIterator[bytes]:
        if self._body_bytes:
            yield self._body_bytes
