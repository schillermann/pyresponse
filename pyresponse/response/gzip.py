"""Gzip response decorator in Pure OOP."""

import zlib
from typing import AsyncIterator

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response
from pyresponse.response.without_header import WithoutHeader


class GzipStream:
    """Async iterator streaming gzip-compressed bytes from an origin stream."""

    def __init__(self, origin_body: AsyncIterator[bytes]) -> None:
        self._origin_body = origin_body

    async def __aiter__(self) -> AsyncIterator[bytes]:
        compressor = zlib.compressobj(level=6, method=zlib.DEFLATED, wbits=31)
        async for chunk in self._origin_body:
            if chunk:
                compressed = compressor.compress(chunk)
                if compressed:
                    yield compressed
        tail = compressor.flush()
        if tail:
            yield tail


class Gzip(Envelope):
    """Response decorator compressing body with gzip and setting Content-Encoding: gzip."""

    def __init__(self, origin: Response) -> None:
        stripped = WithoutHeader(origin, "content-length")
        super().__init__(Header(stripped, "Content-Encoding", "gzip"))

    async def body(self) -> AsyncIterator[bytes]:
        async for chunk in GzipStream(self._origin.body()):
            yield chunk
