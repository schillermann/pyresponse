"""Endpoint protocol interface for request-handling objects."""

from typing import Protocol, runtime_checkable

from pyresponse.request.request import Request
from pyresponse.response.response import Response


@runtime_checkable
class Endpoint(Protocol):
    """Protocol representing an object capable of producing a Response for a Request."""

    async def response(self, req: Request) -> Response:
        """Process the request and return a response."""
        ...
