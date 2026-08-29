"""JSON payload extraction decorator."""

import json
from typing import Any
from pyresponse.request.request import Decorator, Request


class Json(Decorator):
    """Decorator deserializing JSON request body asynchronously."""

    async def data(self) -> Any:
        chunks = []
        async for chunk in self._origin.body():
            chunks.append(chunk)
        raw = b"".join(chunks)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    async def as_dict(self) -> dict[str, Any]:
        data = await self.data()
        if isinstance(data, dict):
            return data
        return {}
