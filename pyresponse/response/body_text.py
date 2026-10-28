"""Response body inspector decoding the asynchronous body stream as a text string."""

from pyresponse.response.body_bytes import BodyBytes
from pyresponse.response.response import Response


class BodyText:
    """Domain object representing the decoded text content of a Response body stream."""

    def __init__(self, response: Response, encoding: str = "utf-8") -> None:
        self._response = response
        self._encoding = encoding

    async def text(self) -> str:
        """Read and decode the response body as a string."""
        raw = await BodyBytes(self._response).bytes()
        return raw.decode(self._encoding)

    async def value(self) -> str:
        """Return the decoded response body string."""
        return await self.text()
