"""Binary streaming HTTP response decorator."""

from typing import AsyncIterable, Iterable

from pyresponse.response.body import Body
from pyresponse.response.content_type import ContentType
from pyresponse.response.envelope import Envelope
from pyresponse.response.response import Response
from pyresponse.response.statusline.statusline import StatusLine


class Binary(Envelope):
    """Binary data HTTP response decorator."""

    def __init__(
        self,
        stream: bytes | AsyncIterable[bytes] | Iterable[bytes] = b"",
        content_type: str = "application/octet-stream",
        status: int = 200,
    ) -> None:
        super().__init__(StatusLine(ContentType(Body(stream), content_type), status))
