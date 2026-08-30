"""Single query parameter inspection decorator."""

from typing import Sequence

from pyresponse.request.envelope import Envelope
from pyresponse.request.param_not_found import ParamNotFoundError
from pyresponse.request.query_params import QueryParams
from pyresponse.request.request import Request


class QueryParam(Envelope):
    """Decorator inspecting a specific named URL query parameter in a Request."""

    def __init__(self, origin: Request, name: str) -> None:
        self._origin = origin
        self._name = name

    async def value(self) -> str:
        """Return parameter value or fail fast with ParamNotFoundError."""
        all_params = await QueryParams(self._origin).params()
        if self._name in all_params and all_params[self._name]:
            return all_params[self._name][0]
        raise ParamNotFoundError(self._name)

    async def value_or(self, fallback: str) -> str:
        """Return parameter value or explicit fallback string."""
        all_params = await QueryParams(self._origin).params()
        if self._name in all_params and all_params[self._name]:
            return all_params[self._name][0]
        return fallback

    async def values(self) -> Sequence[str]:
        """Return all values associated with this query parameter."""
        all_params = await QueryParams(self._origin).params()
        return all_params.get(self._name, ())

    async def has(self) -> bool:
        """Check if query parameter is present in request."""
        all_params = await QueryParams(self._origin).params()
        return self._name in all_params
