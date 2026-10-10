"""Request decorator reading the entire body stream into raw bytes in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class BodyBytes(Envelope):
    """Decorator reading and caching the body stream of a Request as bytes."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)

    async def read(self) -> bytes:
        """Read and return all bytes from the request body."""
        chunks = [c async for c in self._origin.body()]
        return b"".join(chunks)

    async def text(self, encoding: str = "utf-8", errors: str = "strict") -> str:
        """Read and return body decoded as a text string."""
        raw = await self.read()
        return raw.decode(encoding, errors=errors)
