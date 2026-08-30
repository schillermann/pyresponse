"""Sticky request decorator caching byte stream for repeatable reading."""

from typing import AsyncIterator
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class Sticky(Envelope):
    """Decorator caching request body stream for repeatable, idempotent consumption."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._cache: list[bytes] = []
        self._consumed: list[bool] = [False]

    async def body(self) -> AsyncIterator[bytes]:
        for chunk in self._cache:
            yield chunk
        if self._consumed[0]:
            return
        async for chunk in self._origin.body():
            self._cache.append(chunk)
            yield chunk
        self._consumed[0] = True
