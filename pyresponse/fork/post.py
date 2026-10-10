"""Route fork matching HTTP POST method."""

from typing import Any
from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch


class Post(Method):
    """Route fork matching HTTP POST method."""

    def __init__(self, *args: Any) -> None:
        super().__init__("POST", MethodBranch(*args))
