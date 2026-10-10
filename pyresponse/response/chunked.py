"""Chunked transfer encoding response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response
from pyresponse.response.without_header import WithoutHeader


class Chunked(Envelope):
    """Response decorator setting Transfer-Encoding: chunked and stripping Content-Length."""

    def __init__(self, origin: Response) -> None:
        stripped = WithoutHeader(origin, "content-length")
        super().__init__(Header(stripped, "Transfer-Encoding", "chunked"))
