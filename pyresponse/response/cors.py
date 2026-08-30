"""CORS response decorator."""

from typing import AsyncIterator, Sequence

from pyresponse.response.response import Head, Response


class Cors(Response):
    """Response decorator appending Cross-Origin Resource Sharing (CORS) headers."""

    def __init__(
        self,
        origin: Response,
        allow_origin: str = "*",
        allow_methods: Sequence[str] = ("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"),
        allow_headers: Sequence[str] = ("*",),
        allow_credentials: bool = False,
        max_age: int = 86400,
    ) -> None:
        self._origin = origin
        self._allow_origin = allow_origin
        self._allow_methods = allow_methods
        self._allow_headers = allow_headers
        self._allow_credentials = allow_credentials
        self._max_age = max_age

    async def head(self) -> Head:
        origin_head = await self._origin.head()
        headers = list(origin_head.headers())

        headers.append((b"access-control-allow-origin", self._allow_origin.encode("latin1")))
        headers.append((b"access-control-allow-methods", ", ".join(self._allow_methods).encode("latin1")))
        headers.append((b"access-control-allow-headers", ", ".join(self._allow_headers).encode("latin1")))

        if self._allow_credentials:
            headers.append((b"access-control-allow-credentials", b"true"))
        if self._max_age > 0:
            headers.append((b"access-control-max-age", str(self._max_age).encode("latin1")))

        return Head(status=origin_head.status(), headers=headers)

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in self._origin.body():
            yield chunk
