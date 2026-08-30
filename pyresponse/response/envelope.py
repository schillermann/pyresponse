"""Response envelope base decorator."""

from typing import AsyncIterator

from pyresponse.response.head import Head
from pyresponse.response.response import Response


class Envelope(Response):
    """Domain envelope delegating all protocol methods to inner response."""

    def __init__(self, origin: Response) -> None:
        self._origin = origin

    async def head(self) -> Head:
        return await self._origin.head()

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk


ResponseEnvelope = Envelope
