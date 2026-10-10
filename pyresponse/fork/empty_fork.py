"""Empty / Null-object Fork in Pure OOP."""

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.fork.route_entry import RouteEntry
from pyresponse.request.request import Request


class EmptyFork(Fork):
    """Null-object fork representing an empty or unmatched routing destination."""

    def matched(self) -> bool:
        return False

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        return ()

    async def route(self, request: Request) -> Endpoint:
        return MissingEndpoint()
