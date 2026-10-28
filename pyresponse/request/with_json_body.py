"""Request decorator attaching serialized JSON body and Content-Type header in Pure OOP."""

import json
from typing import Any, AsyncIterator

from pyresponse.request.envelope import Envelope
from pyresponse.request.head import Head
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithJsonBody(Envelope):
    """Decorator serializing data as JSON payload and setting Content-Type header."""

    def __init__(self, origin: Request, data: Any) -> None:
        super().__init__(origin)
        self._data = data

    async def head(self) -> Head:
        return await WithHeader(self._origin, "Content-Type", "application/json").head()

    async def body(self) -> AsyncIterator[bytes]:
        yield json.dumps(self._data).encode("utf-8")
