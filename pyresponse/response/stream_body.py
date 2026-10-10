"""Stream body response in Pure OOP."""

from typing import Any, AsyncIterable, AsyncIterator
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class StreamBody(Response):
    """Leaf HTTP response streaming asynchronous bytes."""

    def __init__(self, stream: AsyncIterable[bytes]) -> None:
        self._stream = stream

    def matched(self) -> bool:
        return True

    async def response(self, request: Any) -> Response:
        return self

    async def head(self) -> Head:
        return Head(status=200, headers=[])

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._stream:
            yield chunk
