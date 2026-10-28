"""Request decorator encoding MultipartPart objects as RFC 7578 multipart/form-data."""

from collections.abc import Sequence
from typing import AsyncIterator

from pyresponse.request.envelope import Envelope
from pyresponse.request.head import Head
from pyresponse.request.multipart_part import MultipartPart
from pyresponse.request.request import Request
from pyresponse.request.with_header import WithHeader


class WithMultipartBody(Envelope):
    """Decorator attaching an RFC 7578 multipart/form-data body and Content-Type header."""

    def __init__(
        self,
        origin: Request,
        parts: Sequence[MultipartPart],
        boundary: str = "pyresponse-boundary",
    ) -> None:
        super().__init__(origin)
        self._parts = parts
        self._boundary = boundary

    async def head(self) -> Head:
        enriched = WithHeader(
            self._origin,
            "Content-Type",
            f"multipart/form-data; boundary={self._boundary}",
        )
        return await enriched.head()

    async def body(self) -> AsyncIterator[bytes]:
        delimiter = f"--{self._boundary}\r\n".encode("ascii")
        closing = f"--{self._boundary}--\r\n".encode("ascii")
        chunks: list[bytes] = []
        for part in self._parts:
            chunks.append(delimiter)
            chunks.append(part.bytes())
            chunks.append(b"\r\n")
        chunks.append(closing)
        yield b"".join(chunks)
