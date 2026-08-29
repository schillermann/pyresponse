"""Request interface and base implementations."""

from typing import Any, AsyncIterator, Callable, Protocol, runtime_checkable

from pyresponse.request.header import Header


@runtime_checkable
class Request(Protocol):
    """Abstract HTTP Request."""

    async def head(self) -> Header:
        """Provide request header encapsulation."""
        ...

    async def method(self) -> str:
        """Provide HTTP method."""
        ...

    async def path(self) -> str:
        """Provide request path."""
        ...

    async def query_string(self) -> bytes:
        """Provide raw query string."""
        ...

    async def path_params(self) -> dict[str, str]:
        """Provide extracted route path parameters."""
        ...

    async def body(self) -> AsyncIterator[bytes]:
        """Provide an async byte stream of the request payload."""
        ...


class Base(Request):
    """ASGI-based Request implementation."""

    def __init__(self, scope: dict[str, Any], receive: Callable[..., Any]) -> None:
        self._scope = scope
        self._receive = receive

    async def head(self) -> Header:
        return Header(self._scope.get("headers", ()))

    async def method(self) -> str:
        return self._scope.get("method", "GET")

    async def path(self) -> str:
        return self._scope.get("path", "/")

    async def query_string(self) -> bytes:
        return self._scope.get("query_string", b"")

    async def path_params(self) -> dict[str, str]:
        return self._scope.get("path_params", {})

    async def body(self) -> AsyncIterator[bytes]:
        more_body = True
        while more_body:
            message = await self._receive()
            msg_type = message.get("type", "")
            if msg_type == "http.request":
                chunk = message.get("body", b"")
                more_body = message.get("more_body", False)
                if chunk:
                    yield chunk
            elif msg_type == "http.disconnect":
                break


class Decorator(Request):
    """Base decorator delegating all methods to inner request."""

    def __init__(self, origin: Request) -> None:
        self._origin = origin

    async def head(self) -> Header:
        return await self._origin.head()

    async def method(self) -> str:
        return await self._origin.method()

    async def path(self) -> str:
        return await self._origin.path()

    async def query_string(self) -> bytes:
        return await self._origin.query_string()

    async def path_params(self) -> dict[str, str]:
        return await self._origin.path_params()

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk
