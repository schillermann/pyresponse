"""Route fork matching HTTP PUT method."""

from typing import Any
from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch


class Put(Method):
    """Route fork matching HTTP PUT method."""

    def __init__(self, *args: Any) -> None:
        super().__init__("PUT", MethodBranch(*args))
