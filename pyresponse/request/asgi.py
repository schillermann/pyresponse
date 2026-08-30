"""ASGI-based Request implementation."""

from typing import Any, AsyncIterator, Callable

from pyresponse.request.head import Head
from pyresponse.request.request import Request


class Asgi(Request):
    """ASGI-based Request implementation."""

    def __init__(self, scope: dict[str, Any], receive: Callable[..., Any]) -> None:
        self._scope = scope
        self._receive = receive
        self._buffer: list[bytes] = []
        self._consumed = False

    async def head(self) -> Head:
        return Head(self._scope.get("headers", ()))

    async def method(self) -> str:
        return self._scope.get("method", "GET")

    async def path(self) -> str:
        return self._scope.get("path", "/")

    async def query_string(self) -> bytes:
        return self._scope.get("query_string", b"")

    async def path_params(self) -> dict[str, str]:
        return self._scope.get("path_params", {})

    async def body(self) -> AsyncIterator[bytes]:
        for chunk in self._buffer:
            yield chunk
        if self._consumed:
            return
        more_body = True
        while more_body:
            message = await self._receive()
            msg_type = message.get("type", "")
            if msg_type == "http.request":
                chunk = message.get("body", b"")
                more_body = message.get("more_body", False)
                if chunk:
                    self._buffer.append(chunk)
                    yield chunk
                if not more_body:
                    self._consumed = True
            elif msg_type == "http.disconnect":
                self._consumed = True
                break


AsgiRequest = Asgi
