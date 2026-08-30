"""Missing HTTP cookie domain exception."""

from pyresponse.error import Error


class CookieNotFound(Error, KeyError):
    """Raised when a cookie is requested but not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Cookie '{name}' was not found in request")
        self._name = name

    def name(self) -> str:
        return self._name
