"""Attachment response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Attachment(Envelope):
    """Response decorator attaching Content-Disposition: attachment header for file downloads."""

    def __init__(self, origin: Response, filename: str) -> None:
        super().__init__(Header(origin, "Content-Disposition", f'attachment; filename="{filename}"'))
