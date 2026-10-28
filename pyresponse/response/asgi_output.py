"""ASGI 3.0 output channel capturing response status, headers, and body chunks."""

from collections.abc import MutableMapping
from typing import Any

from pyresponse.response.asgi_not_started import AsgiNotStarted
from pyresponse.response.head import Head


class AsgiOutput:
    """In-memory ASGI 3.0 send channel collecting http.response.start and http.response.body."""

    def __init__(self) -> None:
        self._heads: list[Head] = []
        self._chunks: list[bytes] = []

    async def __call__(self, message: MutableMapping[str, Any]) -> None:
        """Record an outgoing ASGI response message."""
        msg_type = message.get("type", "")
        if msg_type == "http.response.start":
            status = int(message.get("status", 200))
            raw_headers = [
                (bytes(k), bytes(v)) for k, v in message.get("headers", ())
            ]
            self._heads.append(Head(status=status, headers=raw_headers))
        elif msg_type == "http.response.body":
            body = bytes(message.get("body", b""))
            if body:
                self._chunks.append(body)

    def head(self) -> Head:
        """Return captured response Head or fail fast with AsgiNotStarted."""
        if not self._heads:
            raise AsgiNotStarted("ASGI application did not send http.response.start")
        return self._heads[0]

    def chunks(self) -> tuple[bytes, ...]:
        """Return captured response body chunks or fail fast with AsgiNotStarted."""
        if not self._heads:
            raise AsgiNotStarted("ASGI application did not send http.response.start")
        return tuple(self._chunks)
