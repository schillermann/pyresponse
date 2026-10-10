"""Request Authorization header inspector decorator in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class Authorization(Envelope):
    """Decorator inspecting the Authorization header of a Request."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._header = Header(origin, "authorization")

    async def value(self) -> str:
        """Return raw Authorization header string or fail fast."""
        return await self._header.value()

    async def value_or(self, fallback: str = "") -> str:
        """Return raw Authorization header string or fallback if missing."""
        return await self._header.value_or(fallback)

    async def has(self) -> bool:
        """Check if Authorization header is present."""
        return await self._header.has()
