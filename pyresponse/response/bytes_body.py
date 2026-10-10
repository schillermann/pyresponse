"""Bytes body response in Pure OOP."""

from typing import Any, AsyncIterator
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class BytesBody(Response):
    """Leaf HTTP response encapsulating raw bytes."""

    def __init__(self, content: bytes = b"") -> None:
        self._content = content

    def matched(self) -> bool:
        return True

    async def response(self, request: Any) -> Response:
        return self

    async def head(self) -> Head:
        return Head(
            status=200,
            headers=[(b"content-length", str(len(self._content)).encode("latin1"))],
        )

    async def body(self) -> AsyncIterator[bytes]:
        if self._content:
            yield self._content
