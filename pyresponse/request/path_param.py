"""Single path parameter inspection decorator."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.param_not_found import ParamNotFound
from pyresponse.request.path_params import PathParams
from pyresponse.request.request import Request


class PathParam(Envelope):
    """Decorator inspecting a specific named route path parameter in a Request."""

    def __init__(self, origin: Request, name: str, pattern: str = "") -> None:
        self._origin = origin
        self._name = name
        self._pattern = pattern

    async def value(self) -> str:
        """Return path parameter value or fail fast with ParamNotFound."""
        all_params = await PathParams(self._origin, self._pattern).params()
        if self._name in all_params:
            return all_params[self._name]
        raise ParamNotFound(self._name)

    async def value_or(self, fallback: str) -> str:
        """Return path parameter value or explicit fallback string."""
        all_params = await PathParams(self._origin, self._pattern).params()
        if self._name in all_params:
            return all_params[self._name]
        return fallback

    async def has(self) -> bool:
        """Check if path parameter is present."""
        all_params = await PathParams(self._origin, self._pattern).params()
        return self._name in all_params
