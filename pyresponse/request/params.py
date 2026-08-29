"""Query and path parameters extraction decorators."""

import re
import urllib.parse
from pyresponse.request.request import Decorator, Request


class QueryParams(Decorator):
    """Decorator parsing URL query parameters."""

    async def params(self) -> dict[str, list[str]]:
        qs = (await self._origin.query_string()).decode("latin1")
        return urllib.parse.parse_qs(qs, keep_blank_values=True)

    async def param(self, name: str, default: str = "") -> str:
        all_params = await self.params()
        if name in all_params and all_params[name]:
            return all_params[name][0]
        return default

    async def param_list(self, name: str) -> list[str]:
        all_params = await self.params()
        return all_params.get(name, [])


class PathParams(Decorator):
    """Decorator extracting path parameters via regex or request metadata."""

    def __init__(self, origin: Request, pattern: str = "") -> None:
        self._origin = origin
        self._pattern = pattern

    async def params(self) -> dict[str, str]:
        existing = await self._origin.path_params()
        if existing:
            return existing
        if self._pattern:
            match = re.match(self._pattern, await self._origin.path())
            if match:
                return match.groupdict()
        return {}

    async def param(self, name: str, default: str = "") -> str:
        p = await self.params()
        return p.get(name, default)


class WithParams(Decorator):
    """Decorator that attaches route path parameters to the Request."""

    def __init__(self, origin: Request, params: dict[str, str]) -> None:
        self._origin = origin
        self._params = params

    async def path_params(self) -> dict[str, str]:
        merged = dict(await self._origin.path_params())
        merged.update(self._params)
        return merged
