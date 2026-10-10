"""Response body payload encapsulation."""

from typing import Any, AsyncIterator

from pyresponse.response.response import Head, Response


class Body(Response):
    """Leaf HTTP response encapsulating a body payload."""

    def __init__(self, content: Any = b"") -> None:
        self._content = content

    def matched(self) -> bool:
        return True

    async def response(self, request: Any = None) -> Response:
        return self

    async def head(self) -> Head:
        headers = []
        if isinstance(self._content, (str, bytes)):
            b = self._content.encode("utf-8") if isinstance(self._content, str) else self._content
            headers.append((b"content-length", str(len(b)).encode("latin1")))
        return Head(status=200, headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        if isinstance(self._content, str):
            if self._content:
                yield self._content.encode("utf-8")
        elif isinstance(self._content, bytes):
            if self._content:
                yield self._content
        elif hasattr(self._content, "__aiter__"):
            async for chunk in self._content:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
        elif hasattr(self._content, "__iter__"):
            for chunk in self._content:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")

