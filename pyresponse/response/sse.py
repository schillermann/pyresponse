"""Server-Sent Events (SSE) HTTP response decorator in Pure OOP."""

import json
from typing import Any, AsyncIterable, AsyncIterator

from pyresponse.response.cached import NoCache
from pyresponse.response.content_type import ContentType
from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Head, Response


class Event:
    """Server-Sent Event domain representation in Pure OOP."""

    def __init__(
        self,
        data: Any = "",
        event: str = "",
        id: str = "",
        retry: int = -1,
    ) -> None:
        self._data = data
        self._event = event
        self._id = id
        self._retry = retry

    def bytes(self) -> bytes:
        parts: list[str] = []
        if self._event:
            parts.append(f"event: {self._event}")
        if self._id:
            parts.append(f"id: {self._id}")
        if self._retry >= 0:
            parts.append(f"retry: {self._retry}")
        data_val = self._data
        if isinstance(data_val, (dict, list)):
            data_val = json.dumps(data_val)
        parts.append(f"data: {data_val}")
        return ("\n".join(parts) + "\n\n").encode("utf-8")


class SseEvent(Event):
    """Alias for Event domain object."""

    pass


class EventChunk:
    """Adapter rendering an event chunk into serialized SSE bytes."""

    def __init__(self, item: Any) -> None:
        self._item = item

    def bytes(self) -> bytes:
        if isinstance(self._item, Event):
            return self._item.bytes()
        if isinstance(self._item, bytes):
            return self._item
        if isinstance(self._item, str):
            if self._item.startswith("data:") or self._item.startswith("event:"):
                return self._item.encode("utf-8") if self._item.endswith("\n\n") else (self._item + "\n\n").encode("utf-8")
            return f"data: {self._item}\n\n".encode("utf-8")
        if isinstance(self._item, dict):
            return Event(
                data=self._item.get("data", ""),
                event=self._item.get("event", ""),
                id=self._item.get("id", ""),
                retry=self._item.get("retry", -1),
            ).bytes()
        return Event(data=str(self._item)).bytes()


class SseStream(Response):
    """Encapsulates raw SSE event formatting and stream iteration."""

    def __init__(self, stream: AsyncIterable[Any]) -> None:
        self._stream = stream

    async def head(self) -> Head:
        return Head(status=200, headers=[])

    async def body(self) -> AsyncIterator[bytes]:
        async for item in self._stream:
            yield EventChunk(item).bytes()


class Sse(Envelope):
    """Server-Sent Events (SSE) stream HTTP response decorator."""

    def __init__(self, stream: AsyncIterable[Any]) -> None:
        super().__init__(
            Header(
                Header(
                    NoCache(ContentType(SseStream(stream), "text/event-stream")),
                    "Connection",
                    "keep-alive",
                ),
                "X-Accel-Buffering",
                "no",
            )
        )
