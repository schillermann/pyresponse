"""201 Created status line decorator."""

from pyresponse.response.response import Decorator, Head


class Created(Decorator):
    """Decorator setting 201 Created status code."""

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        return Head(
            status=201,
            headers=origin_head.headers(),
        )
