"""NoSniff response security decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class NoSniff(Envelope):
    """Response decorator setting X-Content-Type-Options: nosniff."""

    def __init__(self, origin: Response) -> None:
        super().__init__(Header(origin, "X-Content-Type-Options", "nosniff"))
