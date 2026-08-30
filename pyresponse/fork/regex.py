"""Regex URI path matching fork."""

import re
from typing import Any
from collections.abc import Callable as TypingCallable

from pyresponse.fork.adapted import Adapted
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.unmatched import Unmatched
from pyresponse.fork.with_params import WithParams
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.statusline.not_found import NotFound
from pyresponse.response.text import Text


class Regex(Fork):
    """Route fork matching request path using regular expressions and extracting named parameters."""

    def __init__(
        self,
        pattern: str,
        origin: Endpoint | Fork | TypingCallable[[Request], Any],
    ) -> None:
        self._pattern = pattern
        self._origin = origin

    def matched(self) -> bool:
        return True

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        match = re.match(self._pattern, path)
        if match:
            endpoint = await Adapted(self._origin).route(request)
            if endpoint.matched():
                params = match.groupdict()
                return WithParams(endpoint, params) if params else endpoint
        return Unmatched()



    async def response(self, request: Request) -> Response:
        matched = await self.route(request)
        if matched.matched():
            return await matched.response(request)
        return NotFound(Text("Not Found"))
