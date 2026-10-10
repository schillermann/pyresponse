"""Text body response in Pure OOP."""

from typing import Any, AsyncIterator
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class TextBody(Response):
    """Leaf HTTP response encapsulating text content."""

    def __init__(self, text: str = "") -> None:
        self._text = text

    def matched(self) -> bool:
        return True

    async def response(self, request: Any) -> Response:
        return self

    async def head(self) -> Head:
        b = self._text.encode("utf-8")
        return Head(
            status=200,
            headers=[(b"content-length", str(len(b)).encode("latin1"))],
        )

    async def body(self) -> AsyncIterator[bytes]:
        if self._text:
            yield self._text.encode("utf-8")
