"""Response decorator removing a header in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class WithoutHeader(Envelope):
    """Response decorator stripping a specific HTTP header by name."""

    def __init__(self, origin: Response, name: str) -> None:
        super().__init__(origin)
        self._name = name

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        target = self._name.lower().encode("latin1")
        filtered = [
            (k, v) for k, v in origin_head.headers() if k.lower() != target
        ]
        return Head(status=origin_head.status(), headers=filtered)
