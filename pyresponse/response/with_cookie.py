"""Response decorator attaching a Set-Cookie header in Pure OOP."""

from pyresponse.response.cookie import Cookie
from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class WithCookie(Envelope):
    """Response decorator appending a Set-Cookie header."""

    def __init__(self, origin: Response, cookie: Cookie) -> None:
        super().__init__(origin)
        self._cookie = cookie

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())
        headers.append((b"set-cookie", self._cookie.header_value()))
        return Head(status=origin_head.status(), headers=headers)
