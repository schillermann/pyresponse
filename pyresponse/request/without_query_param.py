"""Request decorator removing a query parameter in Pure OOP."""

import urllib.parse
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithoutQueryParam(Envelope):
    """Decorator removing a specific URL query parameter."""

    def __init__(self, origin: Request, name: str) -> None:
        super().__init__(origin)
        self._param_name = name

    async def query_string(self) -> bytes:
        raw_qs = (await self._origin.query_string()).decode("latin1")
        params = urllib.parse.parse_qs(raw_qs, keep_blank_values=True)
        params.pop(self._param_name, None)
        encoded = urllib.parse.urlencode(params, doseq=True)
        return encoded.encode("latin1")
