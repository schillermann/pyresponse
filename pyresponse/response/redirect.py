"""HTTP Redirect response decorator."""

from pyresponse.response.body import Body
from pyresponse.response.envelope import Envelope
from pyresponse.response.location import Location
from pyresponse.response.statusline.statusline import StatusLine


class Redirect(Envelope):
    """HTTP redirect response decorator."""

    def __init__(self, location: str, status: int = 307) -> None:
        super().__init__(StatusLine(Location(Body(b""), location), status))
