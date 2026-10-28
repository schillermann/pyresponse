"""Response body inspector reading the full asynchronous body stream into raw bytes."""

from pyresponse.response.response import Response


class BodyBytes:
    """Domain object representing the full byte content of a Response body stream."""

    def __init__(self, response: Response) -> None:
        self._response = response

    async def bytes(self) -> bytes:
        """Collect and return all body chunks as a single byte string."""
        chunks = [chunk async for chunk in self._response.body()]
        return b"".join(chunks)

    async def value(self) -> bytes:
        """Return the full body bytes."""
        return await self.bytes()
