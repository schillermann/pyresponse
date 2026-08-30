"""ASGI 3.0 application adapter."""

from typing import Any, Callable

from pyresponse.fork.adapted import Adapted
from pyresponse.fork.endpoint import Endpoint
from pyresponse.lifespan.lifespan import Lifespan
from pyresponse.request.asgi import Asgi
from pyresponse.request.request import Request
from pyresponse.request.sticky import Sticky
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
            req = Sticky(Asgi(scope, receive))
            response = await Adapted(self._endpoint).response(req)

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
