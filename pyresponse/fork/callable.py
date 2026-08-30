"""Callable endpoint adapter."""

import inspect
from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.endpoint import Endpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class Callable(Endpoint):
    """Endpoint adapter executing a callable function."""

    def __init__(self, target: TypingCallable[[Request], Any]) -> None:
        self._target = target

    def matched(self) -> bool:
        return True

    async def response(self, request: Request) -> Response:
        res = self._target(request)
        if inspect.isawaitable(res):
            res = await res
        return res


