"""Request body representations."""

from typing import Any, AsyncIterator


class Body:
    """Request body byte stream (defaults to empty byte stream)."""

    def __init__(self, content: Any = b"") -> None:
        self._content = content

    async def stream(self) -> AsyncIterator[bytes]:
        if self._content:
            if isinstance(self._content, bytes):
                yield self._content
            elif isinstance(self._content, str):
                yield self._content.encode("utf-8")
            elif hasattr(self._content, "__aiter__"):
                async for chunk in self._content:
                    yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
            elif hasattr(self._content, "__iter__"):
                for chunk in self._content:
                    yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
        else:
            if False:
                yield b""

    async def read(self) -> bytes:
        if isinstance(self._content, bytes):
            return self._content
        if isinstance(self._content, str):
            return self._content.encode("utf-8")
        chunks = []
        async for c in self.stream():
            chunks.append(c)
        return b"".join(chunks)
