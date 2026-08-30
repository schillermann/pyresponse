"""Sub-path request decorator."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class SubPath(Envelope):
    """Decorator adjusting request path for nested prefix routing."""

    def __init__(self, origin: Request, sub_path: str) -> None:
        super().__init__(origin)
        self._sub_path = sub_path

    async def path(self) -> str:
        return self._sub_path
