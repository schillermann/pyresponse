"""Request decorator attaching Basic auth Authorization header in Pure OOP."""

import base64

from pyresponse.request.envelope import Envelope
from pyresponse.request.head import Head
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithBasicAuth(Envelope):
    """Decorator attaching HTTP Authorization Basic credentials header."""

    def __init__(self, origin: Request, username: str, password: str) -> None:
        super().__init__(origin)
        self._username = username
        self._password = password

    async def head(self) -> Head:
        raw = f"{self._username}:{self._password}".encode("utf-8")
        encoded = base64.b64encode(raw).decode("utf-8")
        return await WithHeader(self._origin, "Authorization", f"Basic {encoded}").head()
