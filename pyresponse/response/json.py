"""JSON HTTP response."""

import json
from typing import Any, AsyncIterator
from pyresponse.response.response import Head, Response


def _default_encoder(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "value"):
        return obj.value
    return str(obj)


class Json(Response):
    """JSON HTTP response serializing payload with UTF-8 encoding."""

    def __init__(self, data: Any, status: int = 200) -> None:
        self._data = data
        self._status = status

    def _encoded(self) -> bytes:
        return json.dumps(self._data, default=_default_encoder).encode("utf-8")

    async def head(self) -> Head:
        raw = self._encoded()
        return Head(
            status=self._status,
            headers=[
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(raw)).encode("latin1")),
            ],
        )

    async def body(self) -> AsyncIterator[bytes]:
        yield self._encoded()
