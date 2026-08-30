"""HTTP Response Head metadata."""


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
