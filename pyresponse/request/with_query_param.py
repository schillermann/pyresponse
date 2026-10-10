"""Request decorator adding or updating a query parameter in Pure OOP."""

import urllib.parse
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithQueryParam(Envelope):
    """Decorator adding or replacing a specific URL query parameter."""

    def __init__(self, origin: Request, name: str, value: str) -> None:
        super().__init__(origin)
        self._param_name = name
        self._param_value = value

    async def query_string(self) -> bytes:
        raw_qs = (await self._origin.query_string()).decode("latin1")
        params = urllib.parse.parse_qs(raw_qs, keep_blank_values=True)
        params[self._param_name] = [self._param_value]
        encoded = urllib.parse.urlencode(params, doseq=True)
        return encoded.encode("latin1")
