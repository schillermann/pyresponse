"""Missing route domain exception."""

from pyresponse.error import Error


class RouteNotFoundError(Error, LookupError):
    """Raised when no matching fork/route is found for an incoming request."""

    def __init__(self, path: str, method: str = "") -> None:
        super().__init__(f"No route found for {method} {path}".strip())
        self._path = path
        self._method = method

    def path(self) -> str:
        return self._path

    def method(self) -> str:
        return self._method


RouteNotFound = RouteNotFoundError
