"""CORS response decorator."""

from typing import Sequence

from pyresponse.response.envelope import Envelope
from pyresponse.response.head import Head
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Cors(Envelope):
    """Response decorator appending Cross-Origin Resource Sharing (CORS) headers."""

    def __init__(
        self,
        origin: Response,
        allow_origin: str = "*",
        allow_methods: Sequence[str] = ("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"),
        allow_headers: Sequence[str] = ("*",),
        allow_credentials: bool = False,
        max_age: int = 86400,
    ) -> None:
        super().__init__(origin)
        self._allow_origin = allow_origin
        self._allow_methods = allow_methods
        self._allow_headers = allow_headers
        self._allow_credentials = allow_credentials
        self._max_age = max_age

    async def head(self) -> Head:
        decorated: Response = Header(
            Header(
                Header(self._origin, "access-control-allow-origin", self._allow_origin),
                "access-control-allow-methods",
                ", ".join(self._allow_methods),
            ),
            "access-control-allow-headers",
            ", ".join(self._allow_headers),
        )
        if self._allow_credentials:
            decorated = Header(decorated, "access-control-allow-credentials", "true")
        if self._max_age > 0:
            decorated = Header(decorated, "access-control-max-age", str(self._max_age))
        return await decorated.head()
