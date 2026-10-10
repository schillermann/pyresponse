"""Endpoint protocol interface for request-handling objects."""

from typing import Protocol, runtime_checkable

from pyresponse.request.request import Request
from pyresponse.response.response import Response


@runtime_checkable
class Endpoint(Protocol):
    """Protocol representing an object capable of producing a Response for a Request."""

    def matched(self) -> bool:
        """Check whether the endpoint was successfully matched."""
        ...

    async def response(self, request: Request) -> Response:
        """Process the request and return a response."""
        ...


@runtime_checkable
class Branch(Protocol):
    """Protocol representing a router branch capable of evaluating requests."""

    async def route(self, request: Request) -> Endpoint:
        """Evaluate the request and return the matching Endpoint."""
        ...


class Envelope(Endpoint):
    """Base class for endpoint decorators implementing the envelope pattern."""

    def __init__(self, origin: Endpoint) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return self._origin.matched()

    async def response(self, request: Request) -> Response:
        return await self._origin.response(request)


