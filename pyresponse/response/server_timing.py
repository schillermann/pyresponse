"""Server-Timing response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class ServerTiming(Envelope):
    """Response decorator attaching the Server-Timing HTTP header."""

    def __init__(self, origin: Response, metric: str = "app", dur: float | int = 0) -> None:
        super().__init__(Header(origin, "Server-Timing", f"{metric};dur={dur}"))
