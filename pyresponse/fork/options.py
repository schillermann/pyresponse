"""Route fork matching HTTP OPTIONS method."""

from typing import Any
from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch


class Options(Method):
    """Route fork matching HTTP OPTIONS method."""

    def __init__(self, *args: Any) -> None:
        super().__init__("OPTIONS", MethodBranch(*args))
