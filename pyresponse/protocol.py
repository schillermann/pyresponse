"""Core protocols and interfaces for pyresponse."""

from typing import Any, AsyncIterator, Protocol, runtime_checkable

from pyresponse.fork.fork import Endpoint, Fork, Page
from pyresponse.request.header import Header
from pyresponse.request.request import Request
from pyresponse.response.response import Head, Response


class Lifespan:
    """Lifespan lifecycle for ASGI startup and shutdown hooks."""

    async def startup(self) -> None:
        """Run on ASGI lifespan.startup."""
        pass

    async def shutdown(self) -> None:
        """Run on ASGI lifespan.shutdown."""
        pass


class FakeLifespan(Lifespan):
    """Fake Lifespan tracking startup and shutdown execution for testing."""

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.stopped = True


__all__ = [
    "Request",
    "Response",
    "Header",
    "Head",
    "Endpoint",
    "Page",
    "Fork",
    "Lifespan",
    "FakeLifespan",
]
