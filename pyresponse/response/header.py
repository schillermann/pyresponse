"""Response header decorator."""

from pyresponse.response.response import Head, Response


class Header(Response):
    """Response decorator setting an HTTP header."""

    def __init__(self, origin: Response, name: str, value: str) -> None:
        self._origin = origin
        self._name = name
        self._value = value

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())
        headers.append((self._name.encode("latin1"), self._value.encode("latin1")))
        return Head(status=origin_head.status(), headers=headers)

    async def body(self):
        async for chunk in self._origin.body():
            yield chunk
