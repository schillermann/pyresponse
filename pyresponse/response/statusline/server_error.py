"""500 Internal Server Error status line decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class ServerError(Envelope):
    """Decorator setting 500 Internal Server Error status code."""

    def __init__(self, origin: Response) -> None:
        super().__init__(StatusLine(origin, 500))
