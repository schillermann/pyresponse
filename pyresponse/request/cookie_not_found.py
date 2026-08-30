"""Cookie not found error."""

from pyresponse.request.param_not_found import ParamNotFoundError


class CookieNotFoundError(ParamNotFoundError):
    """Raised when a required cookie is missing from the request."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._name = name

    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"Cookie '{self._name}' not found in request"


CookieNotFound = CookieNotFoundError
