"""Request decorator attaching path parameters."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithParams(Envelope):

    """Decorator that attaches route path parameters to the Request."""

    def __init__(self, origin: Request, params: dict[str, str]) -> None:
        self._origin = origin
        self._params = params

    async def path_params(self) -> dict[str, str]:
        merged = dict(await self._origin.path_params())
        merged.update(self._params)
        return merged
