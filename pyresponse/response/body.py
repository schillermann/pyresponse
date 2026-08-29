"""Response body decorator."""

from typing import Any, AsyncIterable, AsyncIterator, Iterable
from pyresponse.response.no_content import NoContent
from pyresponse.response.response import Head, Response


class Body(Response):
    """Response encapsulating or attaching body payload."""

    def __init__(
        self,
        content_or_origin: Any,
        content: Any = None,
    ) -> None:
        self._first = content_or_origin
        self._second = content

    async def head(self) -> Head:
        origin = self._first if self._second is not None else NoContent(status=200)
        body_content = self._second if self._second is not None else self._first

        origin_head = await origin.head()
        headers = list(origin_head.headers())
        if isinstance(body_content, (str, bytes)):
            b = body_content.encode("utf-8") if isinstance(body_content, str) else body_content
            has_len = any(k.lower() == b"content-length" for k, _ in headers)
            if not has_len:
                headers.append((b"content-length", str(len(b)).encode("latin1")))
        return Head(status=origin_head.status(), headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        body_content = self._second if self._second is not None else self._first
        if isinstance(body_content, str):
            yield body_content.encode("utf-8")
        elif isinstance(body_content, bytes):
            yield body_content
        elif hasattr(body_content, "__aiter__"):
            async for chunk in body_content:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
        elif hasattr(body_content, "__iter__"):
            for chunk in body_content:
                yield chunk if isinstance(chunk, bytes) else str(chunk).encode("utf-8")
