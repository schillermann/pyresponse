"""ASGI 3.0 HTTP connection scope constructed from a Request."""

from typing import Any

from pyresponse.request.request import Request


class AsgiScope:
    """Domain object representing an ASGI 3.0 HTTP connection scope from a Request."""

    def __init__(self, request: Request) -> None:
        self._request = request

    async def value(self) -> dict[str, Any]:
        """Construct and return the ASGI 3.0 HTTP scope dictionary."""
        req_head = await self._request.head()
        path = await self._request.path()
        headers = [(k.lower(), v) for k, v in req_head.headers()]
        return {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": await self._request.method(),
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("latin1"),
            "query_string": await self._request.query_string(),
            "root_path": "",
            "headers": headers,
            "path_params": dict(await self._request.path_params()),
            "server": ("testserver", 80),
            "client": ("testclient", 50000),
        }
