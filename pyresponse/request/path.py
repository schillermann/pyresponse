"""Request path inspection decorator."""

from pyresponse.request.envelope import Envelope


class Path(Envelope):

    """Decorator inspecting the URI path of a request."""

    async def value(self) -> str:
        """Return URI path of request."""
        return await self._origin.path()

    async def as_string(self) -> str:
        """Backwards compatibility alias for value()."""
        return await self.value()
