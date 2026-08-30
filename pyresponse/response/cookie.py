"""HTTP Cookie domain representation for responses."""

from http.cookies import SimpleCookie


class Cookie:
    """HTTP Cookie domain object encapsulating cookie attributes and formatting."""

    def __init__(
        self,
        name: str,
        value: str = "",
        max_age: int = -1,
        expires: str = "",
        path: str = "/",
        domain: str = "",
        secure: bool = False,
        http_only: bool = False,
        same_site: str = "",
    ) -> None:
        self._name = name
        self._value = value
        self._max_age = max_age
        self._expires = expires
        self._path = path
        self._domain = domain
        self._secure = secure
        self._http_only = http_only
        self._same_site = same_site

    def name(self) -> str:
        """Return cookie name."""
        return self._name

    def value(self) -> str:
        """Return cookie value."""
        return self._value

    def header_value(self) -> bytes:
        """Format and return the RFC-compliant Set-Cookie header bytes."""
        cookie: SimpleCookie[str] = SimpleCookie()
        cookie[self._name] = self._value
        morsel = cookie[self._name]

        if self._max_age >= 0:
            morsel["max-age"] = str(self._max_age)
        if self._expires:
            morsel["expires"] = self._expires
        if self._path:
            morsel["path"] = self._path
        if self._domain:
            morsel["domain"] = self._domain
        if self._secure:
            morsel["secure"] = True
        if self._http_only:
            morsel["httponly"] = True
        if self._same_site:
            morsel["samesite"] = self._same_site

        return morsel.OutputString().encode("latin1")
