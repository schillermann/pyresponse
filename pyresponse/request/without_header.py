"""Request decorator removing a header in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.head import Head
from pyresponse.request.request import Request


class WithoutHeader(Envelope):
    """Decorator stripping a specific HTTP header from the request head."""

    def __init__(self, origin: Request, name: str) -> None:
        super().__init__(origin)
        self._name = name

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        target = self._name.lower().encode("latin1")
        filtered = [
            (k, v) for k, v in origin_head.headers() if k.lower() != target
        ]
        return Head(filtered)
