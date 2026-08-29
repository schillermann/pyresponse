"""HTTP Redirect response."""

from typing import AsyncIterator
from pyresponse.response.response import Head, Response


class Redirect(Response):
    """HTTP redirect response."""

    def __init__(self, location: str, status: int = 307) -> None:
        self._location = location
        self._status = status

    async def head(self) -> Head:
        return Head(
            status=self._status,
            headers=[
                (b"location", self._location.encode("latin1")),
                (b"content-length", b"0"),
            ],
        )

    async def body(self) -> AsyncIterator[bytes]:
        if False:
            yield b""
