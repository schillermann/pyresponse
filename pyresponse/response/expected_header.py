"""Assertion verifying that a Response contains a header with an expected substring."""

from pyresponse.response.assertion import ResponseAssertion
from pyresponse.response.response import Response


class ExpectedHeader(ResponseAssertion):
    """Fail-fast assertion checking the presence and substring of a Response header."""

    def __init__(self, name: str, substring: str = "") -> None:
        self._name = name
        self._substring = substring

    async def verify(self, response: Response) -> None:
        """Verify that the header is present and contains substring or raise AssertionError."""
        head = await response.head()
        if not head.has(self._name):
            raise AssertionError(f"Expected header '{self._name}' to be present")
        actual = head.value(self._name)
        if self._substring not in actual:
            raise AssertionError(
                f"Expected header '{self._name}' to contain '{self._substring}', got '{actual}'"
            )
