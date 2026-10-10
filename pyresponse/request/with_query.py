"""Request decorator attaching or modifying query string parameters."""

from urllib.parse import parse_qsl, urlencode

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithQuery(Envelope):
    """Decorator enriching a Request with additional query parameters."""

    def __init__(self, origin: Request, key: str, value: str) -> None:
        super().__init__(origin)
        self._key = key
        self._value = value

    async def query_string(self) -> bytes:
        raw = await self._origin.query_string()
        existing = parse_qsl(raw.decode("latin1"), keep_blank_values=True)
        existing.append((self._key, self._value))
        return urlencode(existing).encode("latin1")
