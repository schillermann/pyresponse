"""204 No Content status line decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head


class NoContent(Envelope):
    """Decorator setting 204 No Content status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=204,
            headers=origin_head.headers(),
        )
