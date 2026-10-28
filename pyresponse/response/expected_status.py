"""Assertion verifying that a Response has the expected HTTP status code."""

from pyresponse.response.assertion import ResponseAssertion
from pyresponse.response.response import Response


class ExpectedStatus(ResponseAssertion):
    """Fail-fast assertion checking the HTTP status code of a Response."""

    def __init__(self, expected: int) -> None:
        self._expected = expected

    async def verify(self, response: Response) -> None:
        """Verify that the response status equals expected or raise AssertionError."""
        actual = (await response.head()).status()
        if actual != self._expected:
            raise AssertionError(f"Expected status {self._expected}, got {actual}")
