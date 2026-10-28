"""Sticky response decorator caching head and body stream for repeatable consumption."""

from typing import AsyncIterator

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class Sticky(Envelope):
    """Decorator caching Response head and body chunks for repeatable, idempotent reading."""

    def __init__(self, origin: Response) -> None:
        super().__init__(origin)
        self._heads: list[Head] = []
        self._chunks: list[bytes] = []
        self._consumed: list[bool] = [False]

    async def head(self) -> Head:
        if not self._heads:
            self._heads.append(await self._origin.head())
        return self._heads[0]

    async def body(self) -> AsyncIterator[bytes]:
        if not self._consumed[0]:
            if not self._heads:
                self._heads.append(await self._origin.head())
            async for chunk in self._origin.body():
                self._chunks.append(chunk)
            self._consumed[0] = True
        for chunk in self._chunks:
            yield chunk
