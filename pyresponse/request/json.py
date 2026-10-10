"""JSON payload extraction decorator."""

import json
from typing import Any

from pyresponse.request.body_bytes import BodyBytes
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class Json(Envelope):
    """Decorator deserializing JSON request body asynchronously."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._body = BodyBytes(origin)

    async def content(self) -> Any:
        raw = await self._body.read()
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    async def value(self) -> Any:
        return await self.content()

    async def data(self) -> Any:
        """Backwards compatibility alias for content()."""
        return await self.content()

    async def as_dict(self) -> dict[str, Any]:
        data = await self.content()
        if isinstance(data, dict):
            return data
        return {}
