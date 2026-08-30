"""Response decorator attaching a Set-Cookie header."""

from typing import AsyncIterator

from pyresponse.response.cookie import Cookie
from pyresponse.response.response import Head, Response


class WithCookie(Response):
    """Response decorator appending a Set-Cookie header."""

    def __init__(
        self,
        origin: Response,
        cookie: Cookie | str = "",
        name: str = "",
        value: str = "",
        max_age: int = -1,
        expires: str = "",
        path: str = "/",
        domain: str = "",
        secure: bool = False,
        http_only: bool = False,
        same_site: str = "",
    ) -> None:
        self._origin = origin
        cookie_name = name if name else (cookie if isinstance(cookie, str) else "")
        self._cookie = cookie if isinstance(cookie, Cookie) else Cookie(
            name=cookie_name,
            value=value,
            max_age=max_age,
            expires=expires,
            path=path,
            domain=domain,
            secure=secure,
            http_only=http_only,
            same_site=same_site,
        )


    async def head(self) -> Head:
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())
        headers.append((b"set-cookie", self._cookie.header_value()))
        return Head(status=origin_head.status(), headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk

