"""200 OK status line decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head


class Ok(Envelope):
    """Decorator setting 200 OK status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=200,
            headers=origin_head.headers(),
        )


OK = Ok
