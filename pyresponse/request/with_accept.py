"""Request decorator attaching Accept header in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithAccept(Envelope):
    """Decorator attaching an Accept header to a Request."""

    def __init__(self, origin: Request, accept: str) -> None:
        super().__init__(WithHeader(origin, "Accept", accept))
