"""Request decorator overriding body byte stream."""

from typing import Any, AsyncIterator

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithBody(Envelope):
    """Decorator replacing or attaching a body payload to a Request."""

    def __init__(self, origin: Request, content: Any) -> None:
        super().__init__(origin)
        self._content = content

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
