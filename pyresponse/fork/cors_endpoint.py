"""CORS-decorated endpoint in Pure OOP."""

from typing import Sequence

from pyresponse.fork.endpoint import Endpoint, Envelope
from pyresponse.fork.transformed_endpoint import TransformedEndpoint
from pyresponse.response.cors import Cors as CorsResponse


class CorsEndpoint(Envelope):
    """Endpoint decorator wrapping the response with CORS headers."""

    def __init__(
        self,
        origin: Endpoint,
        allow_origin: str = "*",
        allow_methods: Sequence[str] = ("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"),
        allow_headers: Sequence[str] = ("*",),
        allow_credentials: bool = False,
        max_age: int = 86400,
    ) -> None:
        super().__init__(
            TransformedEndpoint(
                origin,
                lambda res: CorsResponse(
                    origin=res,
                    allow_origin=allow_origin,
                    allow_methods=allow_methods,
                    allow_headers=allow_headers,
                    allow_credentials=allow_credentials,
                    max_age=max_age,
                ),
            )
        )
