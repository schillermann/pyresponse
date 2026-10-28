"""Protocol for declarative fail-fast verification of a Response."""

from typing import Protocol, runtime_checkable

from pyresponse.response.response import Response


@runtime_checkable
class ResponseAssertion(Protocol):
    """Abstract assertion object verifying a Response condition in Pure OOP."""

    async def verify(self, response: Response) -> None:
        """Verify response condition or fail fast with AssertionError."""
        ...
