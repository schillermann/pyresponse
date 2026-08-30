"""Missing HTTP header domain exception."""

from pyresponse.error import Error


class HeaderNotFoundError(Error, KeyError):
    """Raised when an HTTP header is requested but not found in the request."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Header '{name}' was not found in request")
        self._name = name

    def name(self) -> str:
        return self._name


HeaderNotFound = HeaderNotFoundError
