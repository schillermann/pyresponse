"""Core Endpoint protocol."""

from typing import Protocol, runtime_checkable

from pyresponse.request.request import Request
from pyresponse.response.response import Response


@runtime_checkable
class Endpoint(Protocol):
    """Concrete web endpoint producing an HTTP Response for an incoming Request."""

    def matched(self) -> bool:
        """Indicate whether this endpoint represents a successful match."""
        return True

    async def route(self, request: Request) -> "Endpoint":
        """Route to this endpoint."""
        return self

    async def response(self, request: Request) -> Response:
        """Produce an HTTP response for the given request."""
        ...


Page = Endpoint
Resource = Endpoint
