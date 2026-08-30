"""Exception trapping fork."""

from typing import Any
from collections.abc import Callable as TypingCallable
from types import MappingProxyType
from typing import Mapping

from pyresponse.fork.adapted import Adapted
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.trapped import Trapped
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Trap(Fork):
    """Routing fork wrapping endpoints with exception traps."""

    def __init__(
        self,
        origin: Endpoint | Fork | TypingCallable[[Request], Any],
        traps: Mapping[type[Exception], TypingCallable[[Exception, Request], Any]] = MappingProxyType({}),
        fallback: TypingCallable[[Exception, Request], Any] | None = None,
    ) -> None:
        self._origin = origin
        self._traps = traps
        self._fallback = fallback

    def matched(self) -> bool:
        return True

    async def route(self, request: Request) -> Endpoint:
        endpoint = await Adapted(self._origin).route(request)
        if endpoint.matched():
            return Trapped(endpoint, self._traps, self._fallback)
        return endpoint



    async def response(self, request: Request) -> Response:
        endpoint = await self.route(request)
        return await endpoint.response(request)


Catch = Trap
