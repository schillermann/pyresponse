"""Response decorator attaching payload body to an existing Response."""

from typing import Any, AsyncIterator

from pyresponse.response.response import Head, Response


class WithBody(Response):
    """Response decorator attaching or replacing body payload on an origin Response."""

    def __init__(self, origin: Response, content: Any) -> None:
        self._origin = origin
        self._content = content

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())
        if isinstance(self._content, (str, bytes)):
            b = self._content.encode("utf-8") if isinstance(self._content, str) else self._content
            has_len = any(k.lower() == b"content-length" for k, _ in headers)
            if not has_len:
                headers.append((b"content-length", str(len(b)).encode("latin1")))
        return Head(status=origin_head.status(), headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        if isinstance(self._content, str):
            yield self._content.encode("utf-8")
        elif isinstance(self._content, bytes):
            yield self._content
        elif hasattr(self._content, "__aiter__"):
            async for chunk in self._content:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
        elif hasattr(self._content, "__iter__"):
            for chunk in self._content:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
