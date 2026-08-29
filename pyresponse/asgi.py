"""ASGI 3.0 implementation for pyresponse."""

import inspect
from typing import Any, Callable

from pyresponse.fork.fork import Endpoint
from pyresponse.protocol import Lifespan
from pyresponse.request.request import Base, Request
from pyresponse.response.response import Response


class AsgiApp:
    """ASGI 3.0 application translating HTTP scopes and lifespan events to pyresponse objects."""

    def __init__(
        self,
        endpoint: Endpoint | Callable[[Request], Any] | Any,
        lifespan: Lifespan = Lifespan(),
    ) -> None:
        self._endpoint = endpoint
        self._lifespan = lifespan

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
    ) -> None:
        scope_type = scope.get("type", "")
        if scope_type == "http":
            req = Base(scope, receive)
            response = self._resolve_endpoint(req)
            if inspect.isawaitable(response):
                response = await response

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

        elif scope_type == "lifespan":
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

    def _resolve_endpoint(self, req: Request) -> Any:
        if callable(self._endpoint):
            return self._endpoint(req)
        if hasattr(self._endpoint, "response"):
            return self._endpoint.response(req)
        if hasattr(self._endpoint, "handle"):
            return self._endpoint.handle(req)
        raise TypeError(
            f"Target {self._endpoint!r} is not callable and does not implement response()"
        )
