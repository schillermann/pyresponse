"""Composite Lifespan combining multiple Lifespans in Pure OOP."""

from collections.abc import Sequence
from pyresponse.lifespan.lifespan import Lifespan


class ForkLifespan(Lifespan):
    """Composite lifespan managing multiple sub-lifespans in sequence."""

    def __init__(self, *lifespans: Lifespan) -> None:
        self._lifespans: Sequence[Lifespan] = lifespans

    async def startup(self) -> None:
        for item in self._lifespans:
            await item.startup()

    async def shutdown(self) -> None:
        for item in reversed(self._lifespans):
            await item.shutdown()
