"""400 Bad Request status line decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head


class BadRequest(Envelope):
    """Decorator setting 400 Bad Request status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=400,
            headers=origin_head.headers(),
        )
