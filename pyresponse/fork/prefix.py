"""Path prefix routing fork in Pure OOP."""

from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.prefix_endpoint import PrefixEndpoint
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry
from pyresponse.fork.sub_path import SubPath
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.request.request import Request



class Prefix(Fork):
    """Route fork matching URI path prefix and delegating to child forks or endpoints."""

    def __init__(
        self,
        prefix: str,
        origin: Endpoint | Fork | TypingCallable[[Request], Any],
    ) -> None:
        self._prefix = prefix
        self._origin = origin

    def matched(self) -> bool:
        return True

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        """Polymorphically produce route entries for this prefix."""
        combined = f"{prefix.rstrip('/')}/{self._prefix.lstrip('/')}"
        return EndpointRoutes(self._origin).routes(combined)

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        prefix = self._prefix.rstrip("/")

        if not prefix:
            sub_path = path if path.startswith("/") else f"/{path}"
        elif path == prefix:
            sub_path = "/"
        elif path.startswith(f"{prefix}/"):
            sub_path = path[len(prefix) :]
            if not sub_path.startswith("/"):
                sub_path = f"/{sub_path}"
        else:
            return MissingEndpoint()

        sub_req = SubPath(request, sub_path)
        matched_endpoint = await SourceEndpoint(self._origin).route(sub_req)

        if matched_endpoint.matched():
            return PrefixEndpoint(matched_endpoint, sub_path)
        return MissingEndpoint()

