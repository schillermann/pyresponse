"""Fake HTTP Request implementation for testing."""

from typing import AsyncIterator
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class Fake(Request):
    """Fake HTTP Request for testing and simulation."""

    def __init__(
        self,
        method: str = "GET",
        path: str = "/",
        query_string: bytes = b"",
        headers: list[tuple[bytes, bytes]] | tuple[tuple[bytes, bytes], ...] = (),
        body_bytes: bytes = b"",
        path_params: dict[str, str] | None = None,
    ) -> None:
        self._method = method
        self._path = path
        self._query_string = query_string
        self._headers = headers if isinstance(headers, Header) else Header(headers)
        self._body_bytes = body_bytes
        self._path_params = {} if path_params is None else path_params

    async def head(self) -> Header:
        return self._headers

    async def method(self) -> str:
        return self._method

    async def path(self) -> str:
        return self._path

    async def query_string(self) -> bytes:
        return self._query_string

    async def path_params(self) -> dict[str, str]:
        return self._path_params

    async def body(self) -> AsyncIterator[bytes]:
        if self._body_bytes:
            yield self._body_bytes
