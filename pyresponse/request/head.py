"""Request HTTP head metadata encapsulation."""

from typing import Sequence
from pyresponse.request.header_not_found import HeaderNotFoundError


class Head:
    """Encapsulation of HTTP request head metadata (headers)."""

    def __init__(
        self,
        headers: Sequence[tuple[bytes, bytes]] = (),
    ) -> None:
        self._headers = headers

    def headers(self) -> Sequence[tuple[bytes, bytes]]:
        """Return raw header key-value byte tuples."""
        return self._headers

    def items(self) -> Sequence[tuple[bytes, bytes]]:
        """Alias for headers() for ASGI compatibility."""
        return self._headers

    def value(self, name: str) -> str:
        """Look up header by name returning string value or failing fast if missing."""
        target = name.lower().encode("latin1")
        for k, v in self._headers:
            if k.lower() == target:
                return v.decode("latin1")
        raise HeaderNotFoundError(name)

    def value_or(self, name: str, fallback: str) -> str:
        """Look up header by name returning string value or fallback if missing."""
        target = name.lower().encode("latin1")
        for k, v in self._headers:
            if k.lower() == target:
                return v.decode("latin1")
        return fallback

    def has(self, name: str) -> bool:
        """Check if header is present."""
        target = name.lower().encode("latin1")
        return any(k.lower() == target for k, _ in self._headers)
