"""Base response envelope decorator."""

from typing import AsyncIterator

from pyresponse.response.response import Head, Response


class Envelope(Response):
    """Base class for response decorators implementing the envelope pattern."""

    def __init__(self, origin: Response) -> None:
        self._origin = origin

    async def head(self) -> Head:
        return await self._origin.head()

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk
