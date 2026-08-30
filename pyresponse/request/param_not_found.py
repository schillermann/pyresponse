"""Missing parameter domain exception."""

from pyresponse.error import Error


class ParamNotFoundError(Error, KeyError):
    """Raised when a query or path parameter is requested but not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Parameter '{name}' was not found in request")
        self._name = name

    def name(self) -> str:
        return self._name


ParamNotFound = ParamNotFoundError
