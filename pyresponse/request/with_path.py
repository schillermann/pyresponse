"""Request decorator overriding HTTP request path."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class WithPath(Envelope):
    """Decorator overriding the request URI path."""

    def __init__(self, origin: Request, path: str) -> None:
        super().__init__(origin)
        self._path = path if path.startswith("/") else f"/{path}"

    async def path(self) -> str:
        return self._path
