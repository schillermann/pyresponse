"""Server-Sent Events (SSE) HTTP response."""

import json
from typing import Any, AsyncIterable, AsyncIterator
from pyresponse.response.response import Head, Response


class Sse(Response):
    """Server-Sent Events (SSE) stream HTTP response."""

    def __init__(self, stream: AsyncIterable[str | bytes | dict[str, Any]]) -> None:
        self._stream = stream

    async def head(self) -> Head:
        return Head(
            status=200,
            headers=[
                (b"content-type", b"text/event-stream"),
                (b"cache-control", b"no-cache"),
                (b"connection", b"keep-alive"),
                (b"x-accel-buffering", b"no"),
            ],
        )

    async def body(self) -> AsyncIterator[bytes]:
        async for item in self._stream:
            if isinstance(item, bytes):
                yield item
            elif isinstance(item, str):
                if item.startswith("data:") or item.startswith("event:"):
                    yield item.encode("utf-8") if item.endswith("\n\n") else (item + "\n\n").encode("utf-8")
                else:
                    yield f"data: {item}\n\n".encode("utf-8")
            elif isinstance(item, dict):
                parts = []
                if "event" in item:
                    parts.append(f"event: {item['event']}")
                if "id" in item:
                    parts.append(f"id: {item['id']}")
                if "retry" in item:
                    parts.append(f"retry: {item['retry']}")
                data_val = item.get("data", "")
                if isinstance(data_val, (dict, list)):
                    data_val = json.dumps(data_val)
                parts.append(f"data: {data_val}")
                yield ("\n".join(parts) + "\n\n").encode("utf-8")
