"""ASGI 3.0 interfaces and composable decorators in Pure OOP."""

from collections.abc import Callable, MutableMapping
from typing import Any, Protocol, runtime_checkable

from pyresponse.cli.output import ConsoleOutput, Output
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.lifespan.lifespan import Lifespan
from pyresponse.request.asgi import Asgi
from pyresponse.request.request import Request
from pyresponse.request.sticky import Sticky


@runtime_checkable
class AsgiCallable(Protocol):
    """Protocol representing an ASGI 3.0 callable application."""

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        ...


class AsgiEnvelope(AsgiCallable):
    """Base decorator for ASGI 3.0 applications implementing the envelope pattern."""

    def __init__(self, origin: AsgiCallable) -> None:
        self._origin = origin

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        await self._origin(scope, receive, send)


class AsgiHttpApp(AsgiCallable):
    """Core ASGI HTTP handler translating request to Endpoint response."""

    def __init__(self, endpoint: Endpoint | Callable[[Request], Any] | Any) -> None:
        self._endpoint = endpoint

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries from the internal endpoint."""
        return EndpointRoutes(self._endpoint).routes(prefix)

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        if scope.get("type", "") == "http":
            req = Sticky(Asgi(scope, receive))
            response = await SourceEndpoint(self._endpoint).response(req)

            head = await response.head()
            await send({
                "type": "http.response.start",
                "status": head.status(),
                "headers": head.headers(),
            })

            async for chunk in response.body():
                if chunk:
                    await send({
                        "type": "http.response.body",
                        "body": chunk,
                        "more_body": True,
                    })

            await send({
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            })


class WithLifespan(AsgiEnvelope):
    """ASGI application decorator intercepting and executing Lifespan lifecycle hooks."""

    def __init__(self, origin: AsgiCallable, lifespan: Lifespan = Lifespan()) -> None:
        super().__init__(origin)
        self._lifespan = lifespan

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        if scope.get("type") == "lifespan":
            while True:
                message = await receive()
                msg_type = message.get("type")
                if msg_type == "lifespan.startup":
                    try:
                        await self._lifespan.startup()
                        await send({"type": "lifespan.startup.complete"})
                    except Exception as exc:
                        await send({"type": "lifespan.startup.failed", "message": str(exc)})
                elif msg_type == "lifespan.shutdown":
                    try:
                        await self._lifespan.shutdown()
                        await send({"type": "lifespan.shutdown.complete"})
                    except Exception as exc:
                        await send({"type": "lifespan.shutdown.failed", "message": str(exc)})
                    return
        else:
            await self._origin(scope, receive, send)


class LoggedAsgi(AsgiEnvelope):
    """ASGI application decorator logging HTTP requests and response status codes."""

    def __init__(self, origin: AsgiCallable, output: Output = ConsoleOutput()) -> None:
        super().__init__(origin)
        self._output = output

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        if scope.get("type") == "http":
            method = scope.get("method", "UNKNOWN")
            path = scope.get("path", "/")
            captured_status = 200

            async def logged_send(message: MutableMapping[str, Any]) -> None:
                nonlocal captured_status
                if message.get("type") == "http.response.start":
                    captured_status = message.get("status", 200)
                await send(message)

            await self._origin(scope, receive, logged_send)
            self._output.print(f"{method} {path} -> {captured_status}")
        else:
            await self._origin(scope, receive, send)


class AsgiApp(WithLifespan):
    """ASGI application combining HTTP request routing and Lifespan lifecycle hooks."""

    def __init__(
        self,
        endpoint: Endpoint | Callable[[Request], Any] | Any,
        lifespan: Lifespan = Lifespan(),
    ) -> None:
        self._raw_endpoint = endpoint
        super().__init__(AsgiHttpApp(endpoint), lifespan)

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries from the internal endpoint."""
        return EndpointRoutes(self._raw_endpoint).routes(prefix)
