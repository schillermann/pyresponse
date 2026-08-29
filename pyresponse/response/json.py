"""JSON HTTP response."""

import json
from typing import Any, AsyncIterator
from pyresponse.response.response import Head, Response


class Json(Response):
    """JSON HTTP response serializing payload with UTF-8 encoding."""

    def __init__(self, data: Any, status: int = 200) -> None:
        self._data = data
        self._status = status

    async def head(self) -> Head:
        raw = json.dumps(self._data).encode("utf-8")
        return Head(
            status=self._status,
            headers=[
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(raw)).encode("latin1")),
            ],
        )

    async def body(self) -> AsyncIterator[bytes]:
        yield json.dumps(self._data).encode("utf-8")
