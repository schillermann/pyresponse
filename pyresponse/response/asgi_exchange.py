"""Single in-memory ASGI 3.0 HTTP exchange."""

from collections.abc import Callable, MutableMapping
from typing import Any

from pyresponse.request.request import Request
from pyresponse.response.asgi_input import AsgiInput
from pyresponse.response.asgi_output import AsgiOutput
from pyresponse.response.asgi_scope import AsgiScope


class AsgiExchange:
    """In-memory exchange between a Request and an ASGI 3.0 application."""

    def __init__(
        self,
        app: Callable[
            [MutableMapping[str, Any], Callable[..., Any], Callable[..., Any]],
            Any,
        ],
        request: Request,
    ) -> None:
        self._app = app
        self._request = request

    async def output(self) -> AsgiOutput:
        """Execute the ASGI application once and return the captured AsgiOutput."""
        scope = await AsgiScope(self._request).value()
        req_chunks = [chunk async for chunk in self._request.body()]
        channel_in = AsgiInput(req_chunks)
        channel_out = AsgiOutput()
        await self._app(scope, channel_in, channel_out)
        return channel_out
