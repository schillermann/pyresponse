"""URL-encoded request body decorator."""

import urllib.parse

from pyresponse.request.body_bytes import BodyBytes
from pyresponse.request.envelope import Envelope
from pyresponse.request.form import Form
from pyresponse.request.request import Request


class UrlEncoded(Envelope):
    """Decorator parsing application/x-www-form-urlencoded request body."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._body = BodyBytes(origin)

    async def form(self) -> Form:
        raw = await self._body.read()
        if not raw:
            return Form()
        qs = raw.decode("utf-8", errors="replace")
        fields = urllib.parse.parse_qs(qs, keep_blank_values=True)
        return Form(fields=fields)

    async def field(self, name: str) -> str:
        """Return single field value or fail fast with FieldNotFound."""
        f = await self.form()
        return f.field(name)

    async def field_or(self, name: str, fallback: str) -> str:
        """Return single field value or explicit fallback string."""
        f = await self.form()
        return f.field_or(name, fallback=fallback)

    async def has(self, name: str) -> bool:
        """Check if field is present."""
        f = await self.form()
        return f.has(name)


