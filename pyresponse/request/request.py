"""Core Request protocol."""

from typing import AsyncIterator, Protocol, runtime_checkable

from pyresponse.request.head import Head


@runtime_checkable
class Request(Protocol):
    """Abstract HTTP Request."""

    async def head(self) -> Head:
        """Provide request head metadata encapsulation."""
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
