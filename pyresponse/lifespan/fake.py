"""Fake Lifespan for testing."""

from pyresponse.lifespan.lifespan import Lifespan


class Fake(Lifespan):
    """Fake Lifespan tracking startup and shutdown execution for testing."""

    def __init__(self) -> None:
        self._started = False
        self._shutdown_called = False

    async def startup(self) -> None:
        self._started = True

    async def shutdown(self) -> None:
        self._shutdown_called = True

    def started(self) -> bool:
        """Check if startup lifecycle was executed."""
        return self._started

    def shutdown_called(self) -> bool:
        """Check if shutdown lifecycle was executed."""
        return self._shutdown_called

    def stopped(self) -> bool:
        """Alias for shutdown_called()."""
        return self._shutdown_called


FakeLifespan = Fake
