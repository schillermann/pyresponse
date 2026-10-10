"""Response header decorator."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class Header(Envelope):
    """Response decorator setting an HTTP header."""

    def __init__(self, origin: Response, name: str, value: str) -> None:
        super().__init__(origin)
        self._name = name
        self._value = value

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())
        headers.append((self._name.encode("latin1"), self._value.encode("latin1")))
        return Head(status=origin_head.status(), headers=headers)
