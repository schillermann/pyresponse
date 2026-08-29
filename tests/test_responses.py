"""Tests for Response decorators and implementations."""

import pytest

from pyresponse import (
    OK,
    BadRequest,
    Created,
    NoContent,
    NotFound,
    Ok,
    ServerError,
    StatusLine,
)
from pyresponse.response import (
    Binary,
    Body,
    Header,
    Json,
    Redirect,
    Sse,
    Text,
)


@pytest.mark.asyncio
async def test_response_status_line_ok():
    res = OK(Body("Hello"))
    head = await res.head()
    assert head.status() == 200

    chunks = [c async for c in res.body()]
    assert b"".join(chunks) == b"Hello"


@pytest.mark.asyncio
async def test_response_status_line_custom():
    res = StatusLine(Body("Custom"), status=418)
    head = await res.head()
    assert head.status() == 418


@pytest.mark.asyncio
async def test_response_status_line_helpers():
    from pyresponse.response.statusline.bad_request import BadRequest as StatusBadRequest
    from pyresponse.response.statusline.created import Created as StatusCreated
    from pyresponse.response.statusline.not_found import NotFound as StatusNotFound
    from pyresponse.response.statusline.ok import Ok as StatusOk
    from pyresponse.response.statusline.server_error import ServerError as StatusServerError

    for cls, expected_status in [
        (Created, 201),
        (StatusCreated, 201),
        (BadRequest, 400),
        (StatusBadRequest, 400),
        (NotFound, 404),
        (StatusNotFound, 404),
        (ServerError, 500),
        (StatusServerError, 500),
        (StatusOk, 200),
        (OK, 200),
    ]:
        res = cls(Body("status check"))
        head = await res.head()
        assert head.status() == expected_status


@pytest.mark.asyncio
async def test_response_header():
    res = Header(Body("content"), "X-Custom", "Value")
    head = await res.head()
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    assert headers_dict.get("x-custom") == "Value"


@pytest.mark.asyncio
async def test_response_text():
    res = Text("Hello text")
    head = await res.head()
    assert head.status() == 200
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    assert "text/plain; charset=utf-8" in headers_dict.get("content-type", "")

    chunks = [c async for c in res.body()]
    assert b"".join(chunks) == b"Hello text"


@pytest.mark.asyncio
async def test_response_json():
    res = Json({"key": "value", "count": 42})
    head = await res.head()
    assert head.status() == 200
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    assert "application/json; charset=utf-8" in headers_dict.get("content-type", "")

    chunks = [c async for c in res.body()]
    assert b"".join(chunks) == b'{"key": "value", "count": 42}'


@pytest.mark.asyncio
async def test_response_binary():
    res = Binary(b"\x00\x01\x02\x03", content_type="application/octet-stream")
    head = await res.head()
    assert head.status() == 200
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    assert headers_dict.get("content-type") == "application/octet-stream"

    chunks = [c async for c in res.body()]
    assert b"".join(chunks) == b"\x00\x01\x02\x03"


@pytest.mark.asyncio
async def test_response_sse():
    async def event_generator():
        yield "token1"
        yield {"event": "delta", "data": {"text": "token2"}}

    res = Sse(event_generator())
    head = await res.head()
    assert head.status() == 200
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    assert headers_dict.get("content-type") == "text/event-stream"

    chunks = [c async for c in res.body()]
    full_output = b"".join(chunks).decode("utf-8")
    assert "data: token1\n\n" in full_output
    assert 'event: delta\ndata: {"text": "token2"}\n\n' in full_output


@pytest.mark.asyncio
async def test_response_redirect():
    res = Redirect("https://example.com/redirect", status=302)
    head = await res.head()
    assert head.status() == 302
    headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in head.headers()}
    assert headers_dict.get("location") == "https://example.com/redirect"


@pytest.mark.asyncio
async def test_response_no_content():
    res = NoContent(status=204)
    head = await res.head()
    assert head.status() == 204
    chunks = [c async for c in res.body()]
    assert len(chunks) == 0
