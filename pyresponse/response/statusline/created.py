"""201 Created status line decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head


class Created(Envelope):
    """Decorator setting 201 Created status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=201,
            headers=origin_head.headers(),
        )
