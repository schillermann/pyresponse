"""Request path inspection decorator."""

from pyresponse.request.request import Decorator, Request


class Path(Decorator):
    """Decorator inspecting the URI path of a request."""

    async def as_string(self) -> str:
        return await self._origin.path()
