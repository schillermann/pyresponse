"""Single HTTP Cookie inspection decorator."""

from pyresponse.request.cookie_not_found import CookieNotFoundError
from pyresponse.request.cookies import Cookies
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class Cookie(Envelope):
    """Decorator inspecting a specific named HTTP Cookie in a Request."""

    def __init__(self, origin: Request, name: str) -> None:
        self._origin = origin
        self._name = name

    async def value(self) -> str:
        """Return cookie value or fail fast with CookieNotFoundError."""
        all_cookies = await Cookies(self._origin).cookies()
        if self._name in all_cookies:
            return all_cookies[self._name]
        raise CookieNotFoundError(self._name)

    async def value_or(self, fallback: str) -> str:
        """Return cookie value or explicit fallback string."""
        all_cookies = await Cookies(self._origin).cookies()
        if self._name in all_cookies:
            return all_cookies[self._name]
        return fallback

    async def has(self) -> bool:
        """Check if named cookie is present in request."""
        all_cookies = await Cookies(self._origin).cookies()
        return self._name in all_cookies
