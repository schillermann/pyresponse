"""FrameOptions response security decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class FrameOptions(Envelope):
    """Response decorator setting X-Frame-Options header."""

    def __init__(self, origin: Response, option: str = "DENY") -> None:
        super().__init__(Header(origin, "X-Frame-Options", option))
