"""Cookies request envelope."""

from http.cookies import SimpleCookie
from typing import Mapping

from pyresponse.request.cookie_not_found import CookieNotFound
from pyresponse.request.envelope import Envelope
from pyresponse.request.header import Header
from pyresponse.request.request import Request


class Cookies(Envelope):
    """Request envelope extracting HTTP Cookies from the Cookie header."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._header = Header(origin, "cookie")

    async def cookies(self) -> Mapping[str, str]:
        """Parse and return all cookies present in the request."""
        raw_cookie = await self._header.value_or("")
        if not raw_cookie:
            return {}
        simple_cookie: SimpleCookie = SimpleCookie()
        simple_cookie.load(raw_cookie)

        return {k: v.value for k, v in simple_cookie.items()}

    async def cookie(self, name: str) -> str:
        """Return single cookie value or fail fast with CookieNotFound."""
        all_cookies = await self.cookies()
        if name in all_cookies:
            return all_cookies[name]
        raise CookieNotFound(name)

    async def cookie_or(self, name: str, fallback: str) -> str:
        """Return single cookie value or explicit fallback string."""
        all_cookies = await self.cookies()
        if name in all_cookies:
            return all_cookies[name]
        return fallback

    async def has(self, name: str) -> bool:
        """Check if named cookie is present in request."""
        all_cookies = await self.cookies()
        return name in all_cookies
