"""Plain text HTTP response."""

from typing import AsyncIterator
from pyresponse.response.response import Head, Response


class Text(Response):
    """Plain text HTTP response with UTF-8 encoding."""

    def __init__(self, text: str, status: int = 200) -> None:
        self._text = text
        self._status = status

    async def head(self) -> Head:
        encoded = self._text.encode("utf-8")
        return Head(
            status=self._status,
            headers=[
                (b"content-type", b"text/plain; charset=utf-8"),
                (b"content-length", str(len(encoded)).encode("latin1")),
            ],
        )

    async def body(self) -> AsyncIterator[bytes]:
        yield self._text.encode("utf-8")
