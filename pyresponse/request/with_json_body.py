"""Request decorator attaching serialized JSON body and Content-Type header in Pure OOP."""

import json
from typing import Any
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request
from pyresponse.request.with_body import WithBody
from pyresponse.request.with_header import WithHeader


class WithJsonBody(Envelope):
    """Decorator serializing data as JSON payload and setting Content-Type header."""

    def __init__(self, origin: Request, data: Any) -> None:
        payload = json.dumps(data).encode("utf-8")
        super().__init__(WithHeader(WithBody(origin, payload), "Content-Type", "application/json"))
