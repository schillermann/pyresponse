"""Measured endpoint decorator recording execution time in Pure OOP."""

import time
from pyresponse.fork.endpoint import Endpoint, Envelope
from pyresponse.request.request import Request
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class MeasuredEndpoint(Envelope):
    """Endpoint decorator attaching Server-Timing header with response execution latency."""

    def __init__(self, origin: Endpoint, metric: str = "app") -> None:
        self._origin = origin
        self._metric = metric

    async def response(self, request: Request) -> Response:
        start = time.perf_counter()
        res = await self._origin.response(request)
        dur = round((time.perf_counter() - start) * 1000, 2)
        return Header(res, "Server-Timing", f"{self._metric};dur={dur}")

