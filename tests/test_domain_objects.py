"""Tests for real domain objects and fail-fast exception handling."""

import pytest

from pyresponse import (
    HeaderNotFoundError,
    Lifespan,
    ParamNotFoundError,
    RouteNotFoundError,
)

from pyresponse.fork import UnmatchedEndpoint
from pyresponse.request import Body, Fake as FakeRequest, Head, Header


@pytest.mark.asyncio
async def test_header_fail_fast_and_fallback():
    h = Head([(b"content-type", b"application/json")])
    assert h.value("content-type") == "application/json"
    assert h.has("content-type") is True
    assert h.has("x-missing") is False

    # Missing header without default fails fast with HeaderNotFoundError
    with pytest.raises(HeaderNotFoundError) as exc_info:
        h.value("authorization")
    assert exc_info.value.name() == "authorization"

    # Missing header with default returns fallback value
    assert h.value_or("authorization", fallback="Bearer fallback") == "Bearer fallback"




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
    assert ue.matched() is False
    with pytest.raises(RouteNotFoundError) as exc_info:
        await ue.response(FakeRequest(method="GET", path="/"))
    assert exc_info.value.path() == "/"
    assert exc_info.value.method() == "GET"


@pytest.mark.asyncio
async def test_default_lifespan():
    ls = Lifespan()
    await ls.startup()
    await ls.shutdown()


@pytest.mark.asyncio
async def test_domain_wrappers_and_naming():
    from pyresponse.fork import AsEndpoint, Get, Method
    from pyresponse.request import AsgiRequest, Form, Json as RequestJson, RequestEnvelope, UploadFile
    from pyresponse.response import OK, ResponseEnvelope, Text

    # Test AsgiRequest and RequestEnvelope
    async def mock_receive():
        return {"type": "http.request", "body": b'{"hello": "world"}', "more_body": False}

    asgi_req = AsgiRequest(
        {"type": "http", "method": "POST", "path": "/api", "headers": [(b"x-token", b"xyz")]},
        mock_receive,
    )
    enveloped_req = RequestEnvelope(asgi_req)
    assert await enveloped_req.method() == "POST"
    assert await enveloped_req.path() == "/api"
    head = await enveloped_req.head()
    assert head.value("x-token") == "xyz"

    # Test Json.content() and Json.value()
    json_inspector = RequestJson(enveloped_req)
    content = await json_inspector.content()
    assert content == {"hello": "world"}
    assert await json_inspector.value() == {"hello": "world"}

    # Test ResponseEnvelope
    res = OK(Text("enveloped text"))
    enveloped_res = ResponseEnvelope(res)
    head_res = await enveloped_res.head()
    assert head_res.status() == 200
    chunks = [c async for c in enveloped_res.body()]
    assert b"".join(chunks) == b"enveloped text"


    # Test Form domain class
    file_item = UploadFile(filename="doc.pdf", content_type="application/pdf", content=b"%PDF")
    form = Form(fields={"name": ["Doc"]}, files={"doc": [file_item]})
    assert form.field("name") == "Doc"
    assert form.file("doc").filename() == "doc.pdf"

    # Test Method & Get fork
    get_route = Get(lambda req: OK(Text("method ok")))
    assert get_route.matched() is True
    endpoint = await get_route.route(FakeRequest(method="GET"))
    assert endpoint.matched() is True
    not_matched = await get_route.route(FakeRequest(method="POST"))
    assert not_matched.matched() is False


def test_package_version():
    import pyresponse

    assert pyresponse.__version__ == "0.1.0"



