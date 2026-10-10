"""Request decorator attaching User-Agent header in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithUserAgent(Envelope):
    """Decorator attaching a User-Agent header to a Request."""

    def __init__(self, origin: Request, user_agent: str) -> None:
        super().__init__(WithHeader(origin, "User-Agent", user_agent))
