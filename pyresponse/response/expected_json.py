"""Assertion verifying a nested JSON value at a given key/index path in a Response body."""

from collections.abc import Mapping, Sequence
from typing import Any

from pyresponse.response.assertion import ResponseAssertion
from pyresponse.response.body_json import BodyJson
from pyresponse.response.response import Response


class ExpectedJson(ResponseAssertion):
    """Fail-fast assertion checking a nested JSON field or element in a Response body."""

    def __init__(self, path: Sequence[str | int], expected: Any) -> None:
        self._path = path
        self._expected = expected

    async def verify(self, response: Response) -> None:
        """Traverse JSON payload along path and verify value equals expected."""
        current = await BodyJson(response).value()
        for step in self._path:
            if isinstance(current, Mapping) and isinstance(step, str) and step in current:
                current = current[step]
            elif (
                isinstance(current, Sequence)
                and not isinstance(current, (str, bytes))
                and isinstance(step, int)
                and 0 <= step < len(current)
            ):
                current = current[step]
            else:
                raise AssertionError(f"JSON path {tuple(self._path)!r} not found at {step!r}")
        if current != self._expected:
            raise AssertionError(
                f"Expected JSON at {tuple(self._path)!r} to be {self._expected!r}, got {current!r}"
            )
