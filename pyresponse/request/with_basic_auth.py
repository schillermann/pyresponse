"""Request decorator attaching Basic auth Authorization header in Pure OOP."""

import base64
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithBasicAuth(Envelope):
    """Decorator attaching HTTP Authorization Basic credentials header."""

    def __init__(self, origin: Request, username: str, password: str) -> None:
        encoded = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
        super().__init__(WithHeader(origin, "Authorization", f"Basic {encoded}"))
