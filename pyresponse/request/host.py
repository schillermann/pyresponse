"""Request Host inspector decorator in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class Host(Envelope):
    """Decorator inspecting the Host header of a Request."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._header = Header(origin, "host")

    async def value(self) -> str:
        """Return the Host header string or fail fast."""
        return await self._header.value()

    async def hostname(self) -> str:
        """Return host without port portion."""
        raw = await self.value()
        return raw.split(":")[0].strip().lower()

    async def has(self) -> bool:
        """Check if Host header is present."""
        return await self._header.has()
