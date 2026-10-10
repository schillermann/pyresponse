"""Base response envelope decorator."""

from typing import Any, AsyncIterator

from pyresponse.response.response import Head, Response


class Envelope(Response):
    """Base class for response decorators implementing the envelope pattern."""

    def __init__(self, origin: Response) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return True

    async def response(self, request: Any = None) -> Response:
        return self

    async def head(self) -> Head:
        return await self._origin.head()

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk
