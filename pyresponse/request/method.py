"""HTTP Method inspection decorator."""

from pyresponse.request.envelope import Envelope


class Method(Envelope):

    """Decorator inspecting the HTTP method of a request."""

    async def value(self) -> str:
        """Return HTTP method as uppercase string."""
        return (await self._origin.method()).upper()

    async def as_string(self) -> str:
        """Backwards compatibility alias for value()."""
        return await self.value()
