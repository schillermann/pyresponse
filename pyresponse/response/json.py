"""JSON HTTP response decorator."""

import json
from typing import Any, AsyncIterator

from pyresponse.response.content_type import ContentType
from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class JsonPrimitive:
    """JSON-serializable primitive representation of domain objects."""

    def __call__(self, obj: Any) -> Any:
        if hasattr(obj, "model_dump"):
            return obj.model_dump(mode="json")
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if hasattr(obj, "value"):
            return obj.value
        return str(obj)


class JsonPayload(Response):
    """Lazy JSON payload serialized to bytes only upon demand."""

    def __init__(self, data: Any, primitive: Any = JsonPrimitive()) -> None:
        self._data = data
        self._primitive = primitive

    async def head(self) -> Head:
        return Head(status=200, headers=[])

    async def body(self) -> AsyncIterator[bytes]:
        serialized = json.dumps(self._data, default=self._primitive).encode("utf-8")
        yield serialized


class Json(Envelope):
    """JSON HTTP response decorator serializing payload with UTF-8 encoding."""

    def __init__(self, data: Any, status: int = 200) -> None:
        super().__init__(
            StatusLine(
                ContentType(JsonPayload(data), "application/json; charset=utf-8"),
                status,
            )
        )
