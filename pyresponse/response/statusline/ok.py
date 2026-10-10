"""200 OK HTTP response envelope in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class Ok(Envelope):
    """200 OK HTTP response envelope."""

    def __init__(self, origin: Response) -> None:
        super().__init__(StatusLine(origin, 200))
