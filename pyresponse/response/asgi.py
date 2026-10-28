"""In-memory ASGI 3.0 Response executing an ASGI application against a Request."""

from collections.abc import Callable, MutableMapping
from typing import Any, AsyncIterator

from pyresponse.request.request import Request
from pyresponse.response.asgi_exchange import AsgiExchange
from pyresponse.response.asgi_output import AsgiOutput
from pyresponse.response.head import Head
from pyresponse.response.response import Response


class Asgi(Response):
    """Response produced by invoking an ASGI 3.0 application in memory with a Request."""

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
        self._outputs: list[AsgiOutput] = []

    async def head(self) -> Head:
        """Execute ASGI app lazily on first access and return response Head."""
        if not self._outputs:
            self._outputs.append(await AsgiExchange(self._app, self._request).output())
        return self._outputs[0].head()

    async def body(self) -> AsyncIterator[bytes]:
        """Execute ASGI app lazily on first access and yield response body chunks."""
        if not self._outputs:
            self._outputs.append(await AsgiExchange(self._app, self._request).output())
        for chunk in self._outputs[0].chunks():
            yield chunk
