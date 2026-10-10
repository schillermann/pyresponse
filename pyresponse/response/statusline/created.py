"""201 Created status line decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class Created(Envelope):
    """Decorator setting 201 Created status code."""

    def __init__(self, origin: Response) -> None:
        super().__init__(StatusLine(origin, 201))
