"""Request Accept inspector decorator in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class Accept(Envelope):
    """Decorator inspecting the Accept header of a Request."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._header = Header(origin, "accept")

    async def value(self) -> str:
        """Return the Accept header string or fail fast."""
        return await self._header.value()

    async def has(self) -> bool:
        """Check if Accept header is present."""
        return await self._header.has()
