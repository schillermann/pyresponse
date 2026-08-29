"""Fork and Endpoint protocols, composite Fork, and domain entities."""

import inspect
from typing import Any, Awaitable, Callable, Protocol, Sequence, runtime_checkable

from pyresponse.errors import RouteNotFoundError
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline.not_found import NotFound
from pyresponse.response.text import Text


@runtime_checkable
class Endpoint(Protocol):
    """Concrete web endpoint producing an HTTP Response for an incoming Request."""

    def is_matched(self) -> bool:
        """Indicate whether this endpoint represents a successful match."""
        return True

    async def response(self, request: Request) -> Response:
        """Produce an HTTP response for the given request."""
        ...


class CallableEndpoint(Endpoint):
    """Adapter allowing a callable function to act as an Endpoint."""

    def __init__(self, fn: Callable[[Request], Response | Awaitable[Response]]) -> None:
        self._fn = fn

    def is_matched(self) -> bool:
        return True

    async def response(self, request: Request) -> Response:
        res = self._fn(request)
        if inspect.isawaitable(res):
            return await res
        return res


class UnmatchedEndpoint(Endpoint):
    """Domain entity representing an unmatched branch that fails fast when invoked."""

    def is_matched(self) -> bool:
        return False

    async def response(self, request: Request) -> Response:
        path = await request.path()
        method = await request.method()
        raise RouteNotFoundError(path, method)


@runtime_checkable
class Fork(Protocol):
    """Abstract route fork and composite branch evaluator."""

    def __init__(
        self,
        *branches: Any,
        fallback: Endpoint | Callable[[Request], Any] | None = None,
    ) -> None:
        self._branches = branches
        self._fallback = fallback

    def is_matched(self) -> bool:
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
            matched = await branch.route(request)
            if matched.is_matched():
                return matched

        return UnmatchedEndpoint()

    async def response(self, request: Request) -> Response:
        """Act as an Endpoint by evaluating routes and rendering the response."""
        res = await self.route(request)
        if res.is_matched():
            return await res.response(request)

        fallback = getattr(self, "_fallback", None)
        if fallback is not None:
            fb = (
                fallback
                if isinstance(fallback, Endpoint)
                else CallableEndpoint(fallback)
            )
            return await fb.response(request)

        return NotFound(Text("Not Found"))


Page = Endpoint
Resource = Endpoint
CallableResource = CallableEndpoint
UnmatchedResource = UnmatchedEndpoint
