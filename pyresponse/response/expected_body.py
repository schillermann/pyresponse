"""Assertion verifying that a decoded Response body contains an expected text fragment."""

from pyresponse.response.assertion import ResponseAssertion
from pyresponse.response.body_text import BodyText
from pyresponse.response.response import Response


class ExpectedBody(ResponseAssertion):
    """Fail-fast assertion checking that a Response text body contains a fragment."""

    def __init__(self, fragment: str, encoding: str = "utf-8") -> None:
        self._fragment = fragment
        self._encoding = encoding

    async def verify(self, response: Response) -> None:
        """Verify that the decoded response body contains fragment or raise AssertionError."""
        actual = await BodyText(response, self._encoding).text()
        if self._fragment not in actual:
            raise AssertionError(
                f"Expected body to contain '{self._fragment}', got '{actual}'"
            )
