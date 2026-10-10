"""Lifespan decorator attaching a startup hook in Pure OOP."""

import inspect
from collections.abc import Callable
from typing import Any
from pyresponse.lifespan.envelope import Envelope
from pyresponse.lifespan.lifespan import Lifespan


class WithStartup(Envelope):
    """Decorator running a hook during ASGI lifespan startup."""

    def __init__(self, origin: Lifespan, hook: Callable[[], Any]) -> None:
        self._origin = origin
        self._hook = hook

    async def startup(self) -> None:
        await self._origin.startup()
        res = self._hook()
        if inspect.isawaitable(res):
            await res

