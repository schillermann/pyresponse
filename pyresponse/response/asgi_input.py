"""ASGI 3.0 input channel replaying Request body chunks in memory."""

from collections.abc import Sequence
from typing import Any


class AsgiInput:
    """In-memory ASGI 3.0 receive channel producing http.request and http.disconnect events."""

    def __init__(self, chunks: Sequence[bytes]) -> None:
        self._chunks = chunks
        self._index: list[int] = [0]

    async def __call__(self) -> dict[str, Any]:
        """Return next ASGI receive event dictionary."""
        idx = self._index[0]
        self._index[0] = idx + 1
        if not self._chunks and idx == 0:
            return {"type": "http.request", "body": b"", "more_body": False}
        if idx < len(self._chunks):
            return {
                "type": "http.request",
                "body": self._chunks[idx],
                "more_body": idx < len(self._chunks) - 1,
            }
        return {"type": "http.disconnect"}
