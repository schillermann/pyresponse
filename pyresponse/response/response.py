"""Core Response protocols, interfaces, and base decorators."""

from typing import AsyncIterator, Protocol, runtime_checkable


class Head:
    """HTTP Response metadata encapsulating status code and response headers."""

    def __init__(
        self,
        status: int = 200,
        headers: list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...] = (),
    ) -> None:
        self._status = status
        self._headers = headers

    def status(self) -> int:
        """Return HTTP status code (e.g. 200, 404, 500)."""
        return self._status

    def headers(self) -> list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...]:
        """Return raw HTTP response header byte pairs."""
        return self._headers


@runtime_checkable
class Response(Protocol):
    """Abstract HTTP Response representation."""

    async def head(self) -> Head:
        """Return response status code and headers."""
        ...

    async def body(self) -> AsyncIterator[bytes]:
        """Return asynchronous stream of response body chunks."""
        ...


class Decorator(Response):
    """Base decorator wrapping an underlying Response instance."""

    def __init__(self, origin: Response) -> None:
        self._origin = origin

    async def head(self) -> Head:
        return await self._origin.head()

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk
