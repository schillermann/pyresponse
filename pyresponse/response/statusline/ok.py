"""200 OK HTTP response envelope."""

from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class Ok(StatusLine):
    """200 OK HTTP response envelope."""

    def __init__(self, origin: Response) -> None:
        super().__init__(origin, 200)
