"""Domain exceptions for pyresponse adhering to fail-fast Elegant Objects principles."""


class PyResponseError(Exception):
    """Base exception for all pyresponse framework errors."""
    pass


class HeaderNotFoundError(PyResponseError, KeyError):
    """Raised when an HTTP header is requested but not found in the request."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Header '{name}' was not found in request")
        self._name = name

    def name(self) -> str:
        return self._name


class RouteNotFoundError(PyResponseError, LookupError):
    """Raised when no matching fork/route is found for an incoming request."""

    def __init__(self, path: str, method: str = "") -> None:
        super().__init__(f"No route found for {method} {path}".strip())
        self._path = path
        self._method = method

    def path(self) -> str:
        return self._path

    def method(self) -> str:
        return self._method


class ParamNotFoundError(PyResponseError, KeyError):
    """Raised when a query or path parameter is requested but not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Parameter '{name}' was not found in request")
        self._name = name

    def name(self) -> str:
        return self._name
