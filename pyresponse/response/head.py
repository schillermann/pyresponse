from pyresponse.request.header_not_found import HeaderNotFound


class Head:
    """HTTP Response metadata encapsulating status code and response headers."""

    def __init__(
        self,
        status: int = 200,
        headers: list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...] = (),
    ) -> None:
        self._status = status
        self._headers = headers

    def status(self) -> int:
        """Return HTTP status code (e.g. 200, 404, 500)."""
        return self._status

    def headers(self) -> list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...]:
        """Return raw HTTP response header byte pairs."""
        return self._headers

    def has(self, name: str) -> bool:
        """Check if header name is present in response headers."""
        target = name.lower().encode("latin1")
        return any(k.lower() == target for k, _ in self._headers)

    def value(self, name: str) -> str:
        """Return header value as string, or fail fast with HeaderNotFound."""
        target = name.lower().encode("latin1")
        for k, v in reversed(self._headers):
            if k.lower() == target:
                return v.decode("latin1")
        raise HeaderNotFound(name)


    def value_or(self, name: str, fallback: str) -> str:
        """Return header value as string, or explicit fallback if not found."""
        try:
            return self.value(name)
        except HeaderNotFound:
            return fallback

