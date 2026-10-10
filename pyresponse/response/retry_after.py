"""Retry-After response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class RetryAfter(Envelope):
    """Response decorator setting Retry-After header."""

    def __init__(self, origin: Response, seconds: int) -> None:
        super().__init__(Header(origin, "Retry-After", str(seconds)))
