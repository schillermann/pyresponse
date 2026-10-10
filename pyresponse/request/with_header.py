"""Request decorator attaching or overriding HTTP headers."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.head import Head
from pyresponse.request.request import Request


class WithHeader(Envelope):
    """Decorator enriching a Request with an additional or updated HTTP header."""

    def __init__(self, origin: Request, name: str, value: str) -> None:
        super().__init__(origin)
        self._name = name.lower()
        self._value = value

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        raw_headers = list(origin_head.headers())
        filtered = [
            (k, v) for k, v in raw_headers if k.lower() != self._name.encode("latin1")
        ]
        filtered.append((self._name.encode("latin1"), self._value.encode("latin1")))
        return Head(filtered)
