"""Transformed endpoint decorator applying response wrappers in Pure OOP."""

import inspect
from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.endpoint import Endpoint, Envelope
from pyresponse.request.request import Request
from pyresponse.response.response import Response


class TransformedEndpoint(Envelope):
    """Endpoint decorator transforming or wrapping the returned Response."""

    def __init__(
        self,
        origin: Endpoint,
        transformation: TypingCallable[[Response], Any],
    ) -> None:
        self._origin = origin
        self._transformation = transformation

    async def response(self, request: Request) -> Response:
        res = await self._origin.response(request)
        transformed = self._transformation(res)
        if inspect.isawaitable(transformed):
            transformed = await transformed
        return transformed

