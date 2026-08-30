"""Core Response protocol."""

from typing import AsyncIterator, Protocol, runtime_checkable
from pyresponse.response.head import Head


@runtime_checkable
class Response(Protocol):
    """Abstract HTTP Response representation."""

    async def head(self) -> Head:
        """Return response status code and headers."""
        ...

    async def body(self) -> AsyncIterator[bytes]:
        """Return asynchronous stream of response body chunks."""
        ...
