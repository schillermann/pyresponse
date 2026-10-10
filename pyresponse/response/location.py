"""Location response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Location(Envelope):
    """Response decorator setting the Location redirect target header."""

    def __init__(self, origin: Response, url: str) -> None:
        super().__init__(Header(origin, "Location", url))
