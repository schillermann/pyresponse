"""Authentication not found error."""

from pyresponse.request.header_not_found import HeaderNotFoundError


class AuthNotFoundError(HeaderNotFoundError):
    """Raised when required authentication credentials or tokens are missing/invalid."""

    def __init__(self, scheme: str = "Bearer") -> None:
        super().__init__("Authorization")
        self._scheme = scheme

    def scheme(self) -> str:
        return self._scheme

    def __str__(self) -> str:
        return f"Authentication with scheme '{self._scheme}' not found or malformed in request"


AuthNotFound = AuthNotFoundError
