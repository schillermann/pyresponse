"""Tests for CORS response decorator and CORS routing fork."""

import pytest

from pyresponse import Get, OK, Text
from pyresponse.fork.cors import Cors as CorsFork
from pyresponse.request import Fake as FakeRequest
from pyresponse.response.cors import Cors


@pytest.mark.asyncio
async def test_cors_response_decorator():
    res = OK(Text("CORS data"))
    cors_res = Cors(
        res,
        allow_origin="https://example.com",
        allow_methods=("GET", "POST"),
        allow_headers=("Content-Type", "Authorization"),
        allow_credentials=True,
        max_age=3600,
    )
    head = await cors_res.head()
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}

    assert headers_dict.get("access-control-allow-origin") == "https://example.com"
    assert headers_dict.get("access-control-allow-methods") == "GET, POST"
    assert headers_dict.get("access-control-allow-headers") == "Content-Type, Authorization"
    assert headers_dict.get("access-control-allow-credentials") == "true"
    assert headers_dict.get("access-control-max-age") == "3600"


@pytest.mark.asyncio
async def test_cors_fork_preflight_and_routing():
    route = CorsFork(
        Get("/api/data", lambda req: OK(Text("payload"))),
        allow_origin="*",
    )

    # 1. Preflight OPTIONS request handled automatically with 204 NoContent
    options_req = FakeRequest(method="OPTIONS", path="/api/data")
    options_res = await route.response(options_req)
    options_head = await options_res.head()
    assert options_head.status() == 204
    opt_headers = {k.decode("latin1").lower(): v.decode("latin1") for k, v in options_head.headers()}
    assert opt_headers.get("access-control-allow-origin") == "*"

    # 2. Actual GET request routes to handler and decorates response with CORS headers
    get_req = FakeRequest(method="GET", path="/api/data")
    get_res = await route.response(get_req)
    get_head = await get_res.head()
    assert get_head.status() == 200
    get_headers = {k.decode("latin1").lower(): v.decode("latin1") for k, v in get_head.headers()}
    assert get_headers.get("access-control-allow-origin") == "*"

    chunks = [c async for c in get_res.body()]
    assert b"".join(chunks) == b"payload"
