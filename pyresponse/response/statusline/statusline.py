"""Generic status line decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class StatusLine(Envelope):
    """Decorator setting a custom HTTP status code on a Response."""

    def __init__(self, origin: Response, status: int) -> None:
        super().__init__(origin)
        self._status = status

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=self._status,
            headers=origin_head.headers(),
        )
