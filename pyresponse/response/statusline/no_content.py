"""204 No Content status line decorator."""

from pyresponse.response.response import Decorator, Head


class StatusLineNoContent(Decorator):
    """Decorator setting 204 No Content status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=204,
            headers=origin_head.headers(),
        )


NoContent = StatusLineNoContent
