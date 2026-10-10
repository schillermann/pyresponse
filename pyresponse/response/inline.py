"""Inline response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Inline(Envelope):
    """Response decorator attaching Content-Disposition: inline header."""

    def __init__(self, origin: Response, filename: str) -> None:
        super().__init__(Header(origin, "Content-Disposition", f'inline; filename="{filename}"'))
