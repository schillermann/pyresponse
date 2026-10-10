"""Route fork matching HTTP HEAD method."""

from typing import Any
from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch


class Head(Method):
    """Route fork matching HTTP HEAD method."""

    def __init__(self, *args: Any) -> None:
        super().__init__("HEAD", MethodBranch(*args))
