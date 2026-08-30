"""Route not found domain exception."""

from pyresponse.error import Error


class RouteNotFound(Error):
    """Raised when no route matches the request."""

    def __init__(self, path: str = "", method: str = "") -> None:
        super().__init__(f"No route found for {method} '{path}'")
        self._path = path
        self._method = method

    def path(self) -> str:
        return self._path

    def method(self) -> str:
        return self._method
