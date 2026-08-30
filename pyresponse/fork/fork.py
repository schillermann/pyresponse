"""Composite route fork protocol and branch evaluator."""

from typing import Any, Protocol, runtime_checkable

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.unmatched import Unmatched
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline.not_found import NotFound
from pyresponse.response.text import Text


@runtime_checkable
class Fork(Protocol):
    """Abstract route fork and composite branch evaluator."""

    def __init__(
        self,
        *branches: Any,
    ) -> None:
        self._branches = branches

    def matched(self) -> bool:
        return True

    async def route(self, request: Request) -> Endpoint:
        """Evaluate branches in sequence and return the matching Endpoint."""
        branch_list: list[Fork] = []
        for b in getattr(self, "_branches", ()):
            if isinstance(b, (list, tuple)):
                branch_list.extend(b)
            elif isinstance(b, Fork):
                branch_list.append(b)

        for branch in branch_list:
            matched_endpoint = await branch.route(request)
            if matched_endpoint.matched():
                return matched_endpoint

        return Unmatched()

    async def response(self, request: Request) -> Response:
        """Act as an Endpoint by evaluating routes and rendering the response."""
        res = await self.route(request)
        if res.matched():
            return await res.response(request)
        return NotFound(Text("Not Found"))
