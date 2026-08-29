"""HTTP 204 No Content response."""

from typing import AsyncIterator
from pyresponse.response.response import Head, Response


class NoContent(Response):
    """HTTP 204 No Content response with zero body bytes."""

    def __init__(self, status: int = 204) -> None:
        self._status = status

    async def head(self) -> Head:
        return Head(
            status=self._status,
            headers=[(b"content-length", b"0")],
        )

    async def body(self) -> AsyncIterator[bytes]:
        if False:
            yield b""
