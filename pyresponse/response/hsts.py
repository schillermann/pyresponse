"""Strict-Transport-Security (HSTS) response security decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.header import Header
from pyresponse.response.response import Response


class Hsts(Envelope):
    """Response decorator setting Strict-Transport-Security header."""

    def __init__(
        self,
        origin: Response,
        max_age: int = 31536000,
        include_subdomains: bool = True,
        preload: bool = False,
    ) -> None:
        directives = [f"max-age={max_age}"]
        if include_subdomains:
            directives.append("includeSubDomains")
        if preload:
            directives.append("preload")
        super().__init__(Header(origin, "Strict-Transport-Security", "; ".join(directives)))
