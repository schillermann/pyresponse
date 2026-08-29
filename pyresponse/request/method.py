"""HTTP Method inspection decorator."""

from pyresponse.request.request import Decorator, Request


class Method(Decorator):
    """Decorator inspecting the HTTP method of a request."""

    async def as_string(self) -> str:
        return (await self._origin.method()).upper()
