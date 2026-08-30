"""Path prefix routing fork."""

from typing import Any
from collections.abc import Callable as TypingCallable

from pyresponse.fork.as_endpoint import AsEndpoint
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.prefixed import Prefixed as PrefixedEndpoint
from pyresponse.fork.sub_path import SubPath
from pyresponse.fork.unmatched import UnmatchedEndpoint
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline.not_found import NotFound
from pyresponse.response.text import Text


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
            return UnmatchedEndpoint()

        sub_req = SubPath(request, sub_path)
        matched_endpoint = await AsEndpoint(self._origin).route(sub_req)
        if matched_endpoint.matched():
            return PrefixedEndpoint(matched_endpoint, sub_path)
        return UnmatchedEndpoint()

    async def response(self, request: Request) -> Response:
        matched = await self.route(request)
        if matched.matched():
            return await matched.response(request)
        return NotFound(Text("Not Found"))
