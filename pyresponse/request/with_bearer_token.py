"""Request decorator attaching Bearer token Authorization header in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithBearerToken(Envelope):
    """Decorator attaching HTTP Authorization Bearer token header."""

    def __init__(self, origin: Request, token: str) -> None:
        super().__init__(WithHeader(origin, "Authorization", f"Bearer {token}"))
