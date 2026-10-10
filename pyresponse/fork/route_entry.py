"""Domain objects and protocols representing inspected route entries."""

from typing import Any, Protocol, Sequence, runtime_checkable

__all__ = [
    "Routable",
    "RouteEntry",
    "FunctionRoutes",
    "EndpointRoutes",
]


@runtime_checkable
class Routable(Protocol):
    """Protocol for objects capable of describing their routes."""

    def routes(self, prefix: str = "") -> Sequence["RouteEntry"]:
        """Return the sequence of route entries under the given prefix."""
        ...


class RouteEntry:
    """Encapsulates a single inspected HTTP route."""

    def __init__(self, method: str, path: str, handler: str) -> None:
        self._method = method
        self._path = path
        self._handler = handler

    def method(self) -> str:
        return self._method

    def path(self) -> str:
        return self._path

    def handler(self) -> str:
        return self._handler

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RouteEntry):
            return False
        return (
            self._method == other._method
            and self._path == other._path
            and self._handler == other._handler
        )

    def __repr__(self) -> str:
        return f"RouteEntry({self._method!r}, {self._path!r}, {self._handler!r})"


class FunctionRoutes:
    """Adapts a raw callable function or endpoint to the Routable protocol."""

    def __init__(self, fn: Any) -> None:
        self._fn = fn

    def routes(self, prefix: str = "") -> Sequence[RouteEntry]:
        name = getattr(self._fn, "__name__", self._fn.__class__.__name__)
        return (RouteEntry("ANY", prefix if prefix else "/", name),)


class EndpointRoutes:
    """Decorator ensuring an endpoint or callable behaves as Routable."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def routes(self, prefix: str = "") -> tuple[RouteEntry, ...]:
        if isinstance(self._origin, Routable):
            return tuple(self._origin.routes(prefix))
        return tuple(FunctionRoutes(self._origin).routes(prefix))
