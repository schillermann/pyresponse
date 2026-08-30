"""Path parameters extraction decorator."""

import re
from typing import Mapping

from pyresponse.request.envelope import Envelope
from pyresponse.request.param_not_found import ParamNotFound
from pyresponse.request.request import Request


class PathParams(Envelope):
    """Decorator extracting path parameters via regex or request metadata."""

    def __init__(self, origin: Request, pattern: str = "") -> None:
        self._origin = origin
        self._pattern = pattern

    async def params(self) -> Mapping[str, str]:
        existing = await self._origin.path_params()
        if existing:
            return existing
        if self._pattern:
            match = re.match(self._pattern, await self._origin.path())
            if match:
                return match.groupdict()
        return {}

    async def param(self, name: str, default: str = "") -> str:
        """Return single path parameter value, returning default if provided or failing fast."""
        p = await self.params()
        if name in p:
            return p[name]
        if default:
            return default
        raise ParamNotFound(name)

    async def param_or(self, name: str, fallback: str) -> str:
        """Return single path parameter value or explicit fallback string."""
        p = await self.params()
        if name in p:
            return p[name]
        return fallback

    async def has(self, name: str) -> bool:
        """Check if path parameter is present."""
        p = await self.params()
        return name in p
