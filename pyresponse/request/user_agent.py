"""Request User-Agent inspector decorator in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class UserAgent(Envelope):
    """Decorator inspecting the User-Agent header of a Request."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._header = Header(origin, "user-agent")

    async def value(self) -> str:
        """Return the User-Agent header string or fail fast."""
        return await self._header.value()

    async def has(self) -> bool:
        """Check if User-Agent header is present."""
        return await self._header.has()
