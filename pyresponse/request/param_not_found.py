"""Missing HTTP query or path parameter domain exception."""

from pyresponse.error import Error


class ParamNotFound(Error, KeyError):
    """Raised when a parameter is requested but not found in the request."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Parameter '{name}' was not found in request")
        self._name = name

    def name(self) -> str:
        return self._name
