"""Base StatusLine decorator."""

from pyresponse.response.response import Decorator, Head, Response


class StatusLine(Decorator):
    """Decorator setting a custom HTTP status code on a response."""

    def __init__(self, origin: Response, status: int = 200) -> None:
        self._origin = origin
        self._status = status

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=self._status,
            headers=origin_head.headers(),
        )
