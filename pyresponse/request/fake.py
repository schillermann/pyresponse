"""Fake HTTP Request implementation for testing."""

from types import MappingProxyType
from typing import AsyncIterator, Mapping, Sequence
from pyresponse.request.head import Head
from pyresponse.request.request import Request


class Fake(Request):
    """Fake HTTP Request for testing and simulation."""

    def __init__(
        self,
        method: str = "GET",
        path: str = "/",
        query_string: bytes = b"",
        headers: Head | Sequence[tuple[bytes, bytes]] = Head(),
        body_bytes: bytes = b"",
        path_params: Mapping[str, str] = MappingProxyType({}),
    ) -> None:
        self._method = method
        self._path = path
        self._query_string = query_string
        self._headers = headers
        self._body_bytes = body_bytes
        self._path_params = path_params

    async def head(self) -> Head:
        if hasattr(self._headers, "value"):
            return self._headers
        return Head(self._headers)

    async def method(self) -> str:
        return self._method

    async def path(self) -> str:
        return self._path

    async def query_string(self) -> bytes:
        return self._query_string

    async def path_params(self) -> Mapping[str, str]:
        return self._path_params

    async def body(self) -> AsyncIterator[bytes]:
        if self._body_bytes:
            yield self._body_bytes
