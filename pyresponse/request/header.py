"""Request header encapsulation and decorator."""

from typing import Any
from pyresponse.errors import HeaderNotFoundError


class Header:
    """Encapsulation of HTTP request headers."""

    def __init__(
        self,
        headers: list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...] = (),
    ) -> None:
        self._headers = headers

    def items(self) -> list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...]:
        """Return raw header key-value byte tuples."""
        return self._headers

    def value(self, name: str, default: str | None = None) -> str:
        """Look up header by name returning string value or failing fast if missing and no default."""
        target = name.lower().encode("latin1")
        for k, v in self._headers:
            if k.lower() == target:
                return v.decode("latin1")
        if default is not None:
            return default
        raise HeaderNotFoundError(name)

    def as_string(self, name: str, default: str | None = None) -> str:
        """Look up header by name and return string."""
        return self.value(name, default)

    def has(self, name: str) -> bool:
        """Check if header is present."""
        target = name.lower().encode("latin1")
        return any(k.lower() == target for k, _ in self._headers)

    def as_dict(self) -> dict[str, str]:
        """Convert headers to string dictionary."""
        return {
            k.decode("latin1").lower(): v.decode("latin1")
            for k, v in self._headers
        }


class RequestHeader:
    """Decorator to look up a specific header in a Request."""

    def __init__(self, origin: Any, name: str) -> None:
        self._origin = origin
        self._name = name

    async def head(self) -> Header:
        return await self._origin.head()

    async def body(self) -> Any:
        async for chunk in self._origin.body():
            yield chunk

    async def value(self, default: str | None = None) -> str:
        header = await self._origin.head()
        return header.value(self._name, default)

    async def as_string(self, default: str | None = None) -> str:
        header = await self._origin.head()
        return header.as_string(self._name, default)

    async def exists(self) -> bool:
        header = await self._origin.head()
        return header.has(self._name)
