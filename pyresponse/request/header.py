"""Single Request Header inspection decorator."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class Header(Envelope):

    """Decorator inspecting a specific named HTTP header in a Request."""

    def __init__(self, origin: Request, name: str) -> None:
        self._origin = origin
        self._name = name

    async def value(self, default: str = "") -> str:
        """Return header value or default string if provided, failing fast if missing."""
        headers = await self._origin.head()
        if default:
            return headers.value_or(self._name, default)
        return headers.value(self._name)

    async def value_or(self, fallback: str) -> str:
        """Return header value or fallback if missing."""
        headers = await self._origin.head()
        return headers.value_or(self._name, fallback)

    async def as_string(self, default: str = "") -> str:
        """Backwards compatibility alias for value()."""
        return await self.value(default)

    async def has(self) -> bool:
        """Check if header is present in the request."""
        headers = await self._origin.head()
        return headers.has(self._name)

