"""Response decorator verifying one or more ResponseAssertion objects on access."""

from typing import AsyncIterator

from pyresponse.response.assertion import ResponseAssertion
from pyresponse.response.head import Head
from pyresponse.response.response import Response
from pyresponse.response.sticky import Sticky


class Verified(Response):
    """Decorator verifying declarative ResponseAssertion objects against a Response."""

    def __init__(self, origin: Response, *assertions: ResponseAssertion) -> None:
        self._origin = origin
        self._assertions = assertions
        self._checked: list[Response] = []

    async def verify(self) -> None:
        """Run all assertions against a sticky response once or raise AssertionError."""
        if not self._checked:
            sticky = Sticky(self._origin)
            for assertion in self._assertions:
                await assertion.verify(sticky)
            self._checked.append(sticky)

    async def head(self) -> Head:
        await self.verify()
        return await self._checked[0].head()

    async def body(self) -> AsyncIterator[bytes]:
        await self.verify()
        async for chunk in self._checked[0].body():
            yield chunk
