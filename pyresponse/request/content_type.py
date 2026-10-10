"""Request Content-Type inspector decorator in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class ContentType(Envelope):
    """Decorator inspecting the Content-Type header of a Request."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._header = Header(origin, "content-type")

    async def value(self) -> str:
        """Return the raw Content-Type header string or fail fast."""
        return await self._header.value()

    async def mime_type(self) -> str:
        """Return the MIME type portion excluding parameters like charset."""
        raw = await self.value()
        return raw.split(";")[0].strip().lower()

    async def has(self) -> bool:
        """Check if Content-Type header is present."""
        return await self._header.has()
