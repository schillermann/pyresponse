"""Tests for Bearer and Basic authentication extractors."""

import base64
import pytest

from pyresponse.request import (
    AuthNotFound,
    BasicAuth,
    BearerToken,
    Fake as FakeRequest,
    HeaderNotFound,
)


@pytest.mark.asyncio
async def test_bearer_token_extractor():
    req = FakeRequest(headers=[(b"authorization", b"Bearer eyJhbGciOi...secret-token")])
    bearer = BearerToken(req)

    assert await bearer.token() == "eyJhbGciOi...secret-token"
    assert await bearer.has() is True
    assert await bearer.token_or("fallback") == "eyJhbGciOi...secret-token"

    # Missing authorization
    empty_req = FakeRequest()
    empty_bearer = BearerToken(empty_req)
    assert await empty_bearer.has() is False
    assert await empty_bearer.token_or("fallback_token") == "fallback_token"

    with pytest.raises(AuthNotFound) as exc:
        await empty_bearer.token()
    assert exc.value.scheme() == "Bearer"
    assert isinstance(exc.value, HeaderNotFound)

    # Malformed authorization
    malformed_req = FakeRequest(headers=[(b"authorization", b"Basic 12345")])
    assert await BearerToken(malformed_req).has() is False


@pytest.mark.asyncio
async def test_basic_auth_extractor():
    credentials = base64.b64encode(b"admin:secret_pass123").decode("ascii")
    req = FakeRequest(headers=[(b"authorization", f"Basic {credentials}".encode("latin1"))])
    basic = BasicAuth(req)

    assert await basic.has() is True
    assert await basic.username() == "admin"
    assert await basic.password() == "secret_pass123"
    assert await basic.credentials() == ("admin", "secret_pass123")

    # Missing / Invalid credentials
    empty_req = FakeRequest()
    assert await BasicAuth(empty_req).has() is False

    with pytest.raises(AuthNotFound) as exc:
        await BasicAuth(empty_req).username()
    assert exc.value.scheme() == "Basic"
