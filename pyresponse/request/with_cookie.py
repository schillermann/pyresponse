"""Request decorator attaching HTTP Cookie header in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.head import Head
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithCookie(Envelope):
    """Decorator attaching or appending an HTTP Cookie to a Request."""

    def __init__(self, origin: Request, name: str, value: str) -> None:
        super().__init__(origin)
        self._cookie_header = Header(origin, "cookie")
        self._name = name
        self._value = value

    async def head(self) -> Head:
        existing = await self._cookie_header.value_or("")
        cookie_entry = f"{self._name}={self._value}"
        combined = f"{existing}; {cookie_entry}" if existing else cookie_entry
        return await WithHeader(self._origin, "Cookie", combined).head()
