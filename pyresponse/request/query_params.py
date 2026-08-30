"""Query parameters extraction decorator."""

import urllib.parse
from typing import Mapping, Sequence

from pyresponse.request.envelope import Envelope
from pyresponse.request.param_not_found import ParamNotFoundError


class QueryParams(Envelope):
    """Decorator parsing URL query parameters."""

    async def params(self) -> Mapping[str, Sequence[str]]:
        qs = (await self._origin.query_string()).decode("latin1")
        return urllib.parse.parse_qs(qs, keep_blank_values=True)

    async def param(self, name: str, default: str = "") -> str:
        """Return single query parameter value, returning default if provided or failing fast."""
        all_params = await self.params()
        if name in all_params and all_params[name]:
            return all_params[name][0]
        if default:
            return default
        raise ParamNotFoundError(name)

    async def param_or(self, name: str, fallback: str) -> str:
        """Return single query parameter value or explicit fallback string."""
        all_params = await self.params()
        if name in all_params and all_params[name]:
            return all_params[name][0]
        return fallback

    async def param_list(self, name: str) -> Sequence[str]:
        """Return all values associated with a query parameter name."""
        all_params = await self.params()
        return all_params.get(name, ())

    async def has(self, name: str) -> bool:
        """Check if query parameter is present."""
        all_params = await self.params()
        return name in all_params
