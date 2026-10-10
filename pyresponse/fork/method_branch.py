"""Method branch resolving variable method target arguments lazily."""

from typing import Any

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.fork.path import Path
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.request.request import Request


class MethodBranch(Fork):
    """Router branch resolving variable method targets lazily."""

    def __init__(self, *targets: Any) -> None:
        self._targets = targets

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries for targeted branch."""
        if len(self._targets) >= 2:
            return Path(str(self._targets[0]), self._targets[1]).routes(prefix)
        if self._targets:
            return EndpointRoutes(self._targets[0]).routes(prefix)
        return ()

    async def route(self, request: Request) -> Endpoint:
        """Route request lazily matching path or delegating to inner endpoint."""
        if len(self._targets) >= 2:
            return await Path(str(self._targets[0]), self._targets[1]).route(request)
        if self._targets:
            return await SourceEndpoint(self._targets[0]).route(request)
        return MissingEndpoint()
