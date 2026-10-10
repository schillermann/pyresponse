"""Guarded endpoint decorator enforcing access rules in Pure OOP."""

import inspect
from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.endpoint import Endpoint, Envelope
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline import StatusLine
from pyresponse.response.text import Text


class GuardedEndpoint(Envelope):
    """Endpoint decorator checking a guard predicate before delegating to the origin."""

    def __init__(
        self,
        origin: Endpoint,
        guard: TypingCallable[[Request], Any],
        rejection: Response = StatusLine(Text("Forbidden"), 403),
    ) -> None:
        self._origin = origin
        self._guard = guard
        self._rejection = rejection

    async def response(self, request: Request) -> Response:
        passed = self._guard(request)
        if inspect.isawaitable(passed):
            passed = await passed
        if not passed:
            return self._rejection
        return await self._origin.response(request)

