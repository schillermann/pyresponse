"""Missing or invalid authentication credentials exception."""

from pyresponse.request.header_not_found import HeaderNotFound


class AuthNotFound(HeaderNotFound):
    """Raised when authentication credentials are missing or invalid."""

    def __init__(self, scheme: str = "Bearer") -> None:
        super().__init__("Authorization")
        self._scheme = scheme

    def scheme(self) -> str:
        return self._scheme
