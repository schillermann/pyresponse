"""Host header routing fork in Pure OOP."""

from typing import Any, Callable

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.request.host import Host as RequestHost
from pyresponse.request.request import Request


class Host(Fork):
    """Route fork matching the HTTP Host header (e.g. for multi-tenant or subdomain routing)."""

    def __init__(
        self,
        host: str,
        origin: Endpoint | Fork | Callable[[Request], Any],
    ) -> None:
        self._target_host = host.lower()
        self._origin = origin

    def matched(self) -> bool:
        return True

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        return EndpointRoutes(self._origin).routes(prefix)

    async def route(self, request: Request) -> Endpoint:
        host_inspector = RequestHost(request)
        if not await host_inspector.has():
            return MissingEndpoint()
        hostname = await host_inspector.hostname()
        if hostname == self._target_host or (await host_inspector.value()).lower() == self._target_host:
            return await SourceEndpoint(self._origin).route(request)
        return MissingEndpoint()
