"""Binary streaming HTTP response."""

from typing import AsyncIterable, AsyncIterator, Iterable
from pyresponse.response.response import Head, Response


class Binary(Response):
    """Binary data HTTP response."""

    def __init__(
        self,
        stream: bytes | AsyncIterable[bytes] | Iterable[bytes],
        content_type: str = "application/octet-stream",
        status: int = 200,
    ) -> None:
        self._stream = stream
        self._content_type = content_type
        self._status = status

    async def head(self) -> Head:
        headers = [(b"content-type", self._content_type.encode("latin1"))]
        if isinstance(self._stream, bytes):
            headers.append((b"content-length", str(len(self._stream)).encode("latin1")))
        return Head(status=self._status, headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        if isinstance(self._stream, bytes):
            yield self._stream
        elif hasattr(self._stream, "__aiter__"):
            async for chunk in self._stream:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
        elif hasattr(self._stream, "__iter__"):
            for chunk in self._stream:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
