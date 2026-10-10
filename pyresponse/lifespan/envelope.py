"""Base lifespan envelope decorator in Pure OOP."""

from pyresponse.lifespan.lifespan import Lifespan


class Envelope(Lifespan):
    """Base class for lifespan decorators implementing the envelope pattern."""

    def __init__(self, origin: Lifespan) -> None:
        self._origin = origin

    async def startup(self) -> None:
        await self._origin.startup()

    async def shutdown(self) -> None:
        await self._origin.shutdown()
