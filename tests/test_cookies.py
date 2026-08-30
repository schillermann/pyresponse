"""Tests for Cookie inspection and WithCookie/WithoutCookie decorators."""

import pytest

from pyresponse import Ok, Text
from pyresponse.request import Cookie, CookieNotFound, Cookies, Fake as FakeRequest
from pyresponse.response.cookie import Cookie as ResponseCookie
from pyresponse.response.with_cookie import WithCookie
from pyresponse.response.without_cookie import WithoutCookie


@pytest.mark.asyncio
async def test_request_cookie_inspection():
    req = FakeRequest(headers=[(b"cookie", b"session_id=xyz789; theme=dark; user_id=42")])

    cookies = Cookies(req)
    all_cookies = await cookies.cookies()
    assert all_cookies == {"session_id": "xyz789", "theme": "dark", "user_id": "42"}
    assert await cookies.cookie("session_id") == "xyz789"
    assert await cookies.has("theme") is True
    assert await cookies.has("missing") is False
    assert await cookies.cookie_or("missing", fallback="default_val") == "default_val"

    # Single-cookie inspector
    assert await Cookie(req, "session_id").value() == "xyz789"
    assert await Cookie(req, "session_id").has() is True
    assert await Cookie(req, "missing").has() is False
    assert await Cookie(req, "missing").value_or("fallback") == "fallback"

    with pytest.raises(CookieNotFound) as exc:
        await Cookie(req, "missing").value()
    assert exc.value.name() == "missing"


@pytest.mark.asyncio
async def test_with_cookie_and_without_cookie_response():
    res = Ok(Text("Cookie Set"))
    cookie_obj = ResponseCookie(
        name="session_id",
        value="secret123",
        max_age=3600,
        path="/",
        secure=True,
        http_only=True,
        same_site="Lax",
    )
    assert cookie_obj.name() == "session_id"
    assert cookie_obj.value() == "secret123"

    with_cookie = WithCookie(res, cookie_obj)
    head = await with_cookie.head()
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    set_cookie_val = headers_dict.get("set-cookie", "")
    assert "session_id=secret123" in set_cookie_val
    assert "Max-Age=3600" in set_cookie_val
    assert "Path=/" in set_cookie_val
    assert "Secure" in set_cookie_val
    assert "HttpOnly" in set_cookie_val
    assert "SameSite=Lax" in set_cookie_val

    # WithoutCookie invalidates the cookie with Max-Age=0
    without_cookie = WithoutCookie(res, name="session_id", path="/")
    del_head = await without_cookie.head()
    del_headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in del_head.headers()}
    del_cookie_val = del_headers_dict.get("set-cookie", "")
    assert "session_id=" in del_cookie_val
    assert "Max-Age=0" in del_cookie_val
