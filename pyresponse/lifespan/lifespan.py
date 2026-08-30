"""Lifespan lifecycle for ASGI startup and shutdown hooks."""


class Lifespan:
    """Lifespan lifecycle for ASGI startup and shutdown hooks."""

    async def startup(self) -> None:
        """Run on ASGI lifespan.startup."""
        pass

    async def shutdown(self) -> None:
        """Run on ASGI lifespan.shutdown."""
        pass
