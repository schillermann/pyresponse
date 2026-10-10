"""Plain text HTTP response decorator."""

from pyresponse.response.content_type import ContentType
from pyresponse.response.envelope import Envelope
from pyresponse.response.statusline.statusline import StatusLine
from pyresponse.response.text_body import TextBody


class Text(Envelope):
    """Plain text HTTP response decorator with UTF-8 encoding."""

    def __init__(self, text: str = "", status: int = 200) -> None:
        super().__init__(StatusLine(ContentType(TextBody(text), "text/plain; charset=utf-8"), status))
