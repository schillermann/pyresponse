"""Sub-path request decorator in Pure OOP."""

from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request
from pyresponse.request.with_path import WithPath


class SubPath(Envelope):
    """Decorator adjusting request path for nested prefix routing."""

    def __init__(self, origin: Request, sub_path: str) -> None:
        super().__init__(WithPath(origin, sub_path))
