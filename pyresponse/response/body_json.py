"""Response body inspector deserializing the asynchronous body stream from JSON."""

import json
from typing import Any

from pyresponse.response.body_text import BodyText
from pyresponse.response.response import Response


class BodyJson:
    """Domain object representing the parsed JSON value of a Response body stream."""

    def __init__(self, response: Response) -> None:
        self._response = response

    async def value(self) -> Any:
        """Parse and return the decoded JSON value, failing fast on empty or invalid JSON."""
        text = await BodyText(self._response).text()
        return json.loads(text)
