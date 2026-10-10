"""HTTP 204 No Content response decorator."""

from pyresponse.response.body import Body
from pyresponse.response.envelope import Envelope
from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class NoContent(Envelope):
    """HTTP 204 No Content response decorator with zero body bytes."""

    def __init__(self, origin: Response = Body(b""), status: int = 204) -> None:
        statused = StatusLine(origin, status)
        super().__init__(statused)
