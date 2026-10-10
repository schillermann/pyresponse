"""Server runner for pyresponse applications in Pure OOP."""

from collections.abc import Callable, MutableMapping
from typing import Any

from pyresponse.asgi import AsgiApp
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.lifespan.lifespan import Lifespan
from pyresponse.request.request import Request


class Server:
    """Server runner encapsulating the ASGI application and web server execution."""

    def __init__(
        self,
        endpoint: Endpoint | Callable[[Request], Any] | Any,
        host: str = "127.0.0.1",
        port: int = 8000,
        lifespan: Lifespan = Lifespan(),
        log_level: str = "info",
    ) -> None:
        self._endpoint = endpoint
        self._host = host
        self._port = port
        self._lifespan = lifespan
        self._log_level = log_level

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries from the internal endpoint."""
        return EndpointRoutes(self._endpoint).routes(prefix)

    def app(self) -> AsgiApp:
        """Construct the AsgiApp instance."""
        return AsgiApp(self._endpoint, self._lifespan)

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        """Delegate ASGI calls to the internal AsgiApp."""
        await self.app()(scope, receive, send)

    def start(self) -> None:
        """Start the Uvicorn web server."""
        import uvicorn

        uvicorn.run(
            self.app(),
            host=self._host,
            port=self._port,
            log_level=self._log_level,
        )
