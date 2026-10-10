"""Route fork matching HTTP DELETE method."""

from typing import Any
from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch


class Delete(Method):
    """Route fork matching HTTP DELETE method."""

    def __init__(self, *args: Any) -> None:
        super().__init__("DELETE", MethodBranch(*args))
