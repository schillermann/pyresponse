"""Route fork matching HTTP GET method."""

from typing import Any
from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch


class Get(Method):
    """Route fork matching HTTP GET method."""

    def __init__(self, *args: Any) -> None:
        super().__init__("GET", MethodBranch(*args))
