"""Base request envelope decorator."""

from typing import Any, AsyncIterator

from pyresponse.request.head import Head
from pyresponse.request.request import Request


class Envelope(Request):
    """Base class for request decorators implementing the envelope pattern."""

    def __init__(self, origin: Request) -> None:
        self._origin = origin

    async def head(self) -> Head:
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
