"""404 Not Found status line decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head


class NotFound(Envelope):
    """Decorator setting 404 Not Found status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=404,
            headers=origin_head.headers(),
        )
