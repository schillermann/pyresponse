"""ETag response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Etag(Envelope):
    """Response decorator attaching the ETag HTTP header."""

    def __init__(self, origin: Response, etag: str) -> None:
        super().__init__(Header(origin, "ETag", f'"{etag.strip(chr(34))}"'))
