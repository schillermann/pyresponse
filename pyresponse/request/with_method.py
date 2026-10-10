"""Request decorator overriding HTTP method."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithMethod(Envelope):
    """Decorator overriding the request HTTP method."""

    def __init__(self, origin: Request, method: str) -> None:
        super().__init__(origin)
        self._method = method.upper()

    async def method(self) -> str:
        return self._method
