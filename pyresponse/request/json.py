"""JSON payload extraction decorator."""

import json
from typing import Any

from pyresponse.request.envelope import Envelope


class Json(Envelope):

    """Decorator deserializing JSON request body asynchronously."""

    async def content(self) -> Any:
        chunks = []
        async for chunk in self._origin.body():
            chunks.append(chunk)
        raw = b"".join(chunks)
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
