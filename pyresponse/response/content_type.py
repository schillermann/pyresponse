"""Content-Type response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class ContentType(Envelope):
    """Response decorator setting the Content-Type HTTP header."""

    def __init__(self, origin: Response, content_type: str) -> None:
        super().__init__(Header(origin, "Content-Type", content_type))
