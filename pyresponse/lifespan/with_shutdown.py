"""Lifespan decorator attaching a shutdown hook in Pure OOP."""

import inspect
from collections.abc import Callable
from typing import Any
from pyresponse.lifespan.envelope import Envelope
from pyresponse.lifespan.lifespan import Lifespan


class WithShutdown(Envelope):
    """Decorator running a hook during ASGI lifespan shutdown."""

    def __init__(self, origin: Lifespan, hook: Callable[[], Any]) -> None:
        self._origin = origin
        self._hook = hook

    async def shutdown(self) -> None:
        res = self._hook()
        if inspect.isawaitable(res):
            await res
        await self._origin.shutdown()

