"""500 Internal Server Error status line decorator."""

from pyresponse.response.response import Decorator, Head


class ServerError(Decorator):
    """Decorator setting 500 Internal Server Error status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=500,
            headers=origin_head.headers(),
        )
