"""Fake Lifespan for testing."""

from pyresponse.lifespan.lifespan import Lifespan


class Fake(Lifespan):
    """Fake Lifespan that tracks startup and shutdown calls."""

    def __init__(self) -> None:
        self._started = False
        self._stopped = False

    async def startup(self) -> None:
        self._started = True

    async def shutdown(self) -> None:
        self._stopped = True

    def started(self) -> bool:
        return self._started

    def stopped(self) -> bool:
        return self._stopped
