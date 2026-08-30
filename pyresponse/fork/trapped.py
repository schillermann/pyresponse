"""Trapped endpoint decorator executing exception handlers."""

from typing import Any
from collections.abc import Callable as TypingCallable
from types import MappingProxyType
from typing import Mapping

from pyresponse.fork.endpoint import Endpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Trapped(Endpoint):
    """Endpoint decorator catching domain exceptions and delegating to registered handlers."""

    def __init__(
        self,
        origin: Endpoint,
        traps: Mapping[type[Exception], TypingCallable[[Exception, Request], Any]] = MappingProxyType({}),
        fallback: TypingCallable[[Exception, Request], Any] | None = None,
    ) -> None:
        self._origin = origin
        self._traps = traps
        self._fallback = fallback

    def matched(self) -> bool:
        return self._origin.matched()

    async def response(self, request: Request) -> Response:
        import inspect

        try:
            return await self._origin.response(request)
        except Exception as exc:
            for exc_type, handler in self._traps.items():
                if isinstance(exc, exc_type):
                    result = handler(exc, request)
                    if inspect.isawaitable(result):
                        result = await result
                    return result
            if self._fallback is not None:
                result = self._fallback(exc, request)
                if inspect.isawaitable(result):
                    result = await result
                return result
            raise exc


TrappedEndpoint = Trapped
