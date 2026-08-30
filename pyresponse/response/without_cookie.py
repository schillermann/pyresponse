"""Response decorator invalidating / deleting a cookie."""

from typing import AsyncIterator

from pyresponse.response.cookie import Cookie
from pyresponse.response.response import Head, Response


class WithoutCookie(Response):
    """Response decorator invalidating a cookie by setting Max-Age=0 and past expiry."""

    def __init__(
        self,
        origin: Response,
        name: str,
        path: str = "/",
        domain: str = "",
    ) -> None:
        self._origin = origin
        self._name = name
        self._path = path
        self._domain = domain

    async def head(self) -> Head:
        cookie = Cookie(
            name=self._name,
            value="",
            max_age=0,
            expires="Thu, 01 Jan 1970 00:00:00 GMT",
            path=self._path,
            domain=self._domain,
        )
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())
        headers.append((b"set-cookie", cookie.header_value()))
        return Head(status=origin_head.status(), headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk

