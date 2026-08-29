"""Tests for real domain objects and fail-fast exception handling."""

import pytest

from pyresponse import Lifespan
from pyresponse.errors import (
    HeaderNotFoundError,
    ParamNotFoundError,
    RouteNotFoundError,
)
from pyresponse.fork import UnmatchedEndpoint
from pyresponse.request import Body, Fake as FakeRequest, Header


@pytest.mark.asyncio
async def test_header_fail_fast_and_fallback():
    h = Header([(b"content-type", b"application/json")])
    assert h.value("content-type") == "application/json"
    assert h.has("content-type") is True
    assert h.has("x-missing") is False

    # Missing header without default fails fast with HeaderNotFoundError
    with pytest.raises(HeaderNotFoundError) as exc_info:
        h.value("authorization")
    assert exc_info.value.name() == "authorization"

    # Missing header with default returns fallback value
    assert h.value("authorization", default="Bearer fallback") == "Bearer fallback"


@pytest.mark.asyncio
async def test_request_body_default_empty():
    body = Body()
    chunks = [c async for c in body.stream()]
    assert chunks == []
    assert await body.read() == b""

    body_with_data = Body(b"payload")
    assert await body_with_data.read() == b"payload"


@pytest.mark.asyncio
async def test_unmatched_endpoint_fails_fast():
    ue = UnmatchedEndpoint()
    assert ue.is_matched() is False
    with pytest.raises(RouteNotFoundError) as exc_info:
        await ue.response(FakeRequest(method="GET", path="/"))
    assert exc_info.value.path() == "/"
    assert exc_info.value.method() == "GET"


@pytest.mark.asyncio
async def test_default_lifespan():
    ls = Lifespan()
    await ls.startup()
    await ls.shutdown()
