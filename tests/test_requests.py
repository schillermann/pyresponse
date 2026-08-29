"""Tests for Request decorators and parsers."""

import pytest

from pyresponse.errors import HeaderNotFoundError
from pyresponse.request import (
    Base,
    Fake as FakeRequest,
    Header,
    Json,
    Method,
    Multipart,
    Path,
    PathParams,
    QueryParams,
    RequestHeader,
)


@pytest.mark.asyncio
async def test_request_method_and_path():
    req = FakeRequest(method="POST", path="/api/v1/items")
    assert await Method(req).as_string() == "POST"
    assert await Path(req).as_string() == "/api/v1/items"


@pytest.mark.asyncio
async def test_request_header():
    req = FakeRequest(headers=[(b"authorization", b"Bearer token123"), (b"accept", b"application/json")])
    assert await RequestHeader(req, "Authorization").as_string() == "Bearer token123"
    assert await RequestHeader(req, "Accept").as_string() == "application/json"
    assert await RequestHeader(req, "Accept").exists() is True
    assert await RequestHeader(req, "X-Missing").exists() is False

    # Missing header without default fails fast with HeaderNotFoundError
    with pytest.raises(HeaderNotFoundError):
        await RequestHeader(req, "X-Missing").value()

    # Missing header with default returns fallback value
    assert await RequestHeader(req, "X-Missing").as_string(default="fallback") == "fallback"


@pytest.mark.asyncio
async def test_request_query_params():
    req = FakeRequest(query_string=b"page=2&filter=active&tags=python&tags=oop")
    query = QueryParams(req)
    assert await query.param("page") == "2"
    assert await query.param("filter") == "active"
    assert await query.param("missing", default="default_val") == "default_val"
    assert await query.param_list("tags") == ["python", "oop"]


@pytest.mark.asyncio
async def test_request_path_params():
    req = FakeRequest(path="/users/42/posts/100")
    path_params = PathParams(req, pattern=r"^/users/(?P<user_id>\d+)/posts/(?P<post_id>\d+)$")
    params = await path_params.params()
    assert params == {"user_id": "42", "post_id": "100"}
    assert await path_params.param("user_id") == "42"
    assert await path_params.param("post_id") == "100"


@pytest.mark.asyncio
async def test_request_json():
    req = FakeRequest(
        method="POST",
        headers=[(b"content-type", b"application/json")],
        body_bytes=b'{"name": "Alice", "age": 30}',
    )
    json_data = await Json(req).data()
    assert json_data == {"name": "Alice", "age": 30}


@pytest.mark.asyncio
async def test_request_multipart():
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    payload = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="username"\r\n\r\n'
        f"johndoe\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="test.txt"\r\n'
        f"Content-Type: text/plain\r\n\r\n"
        f"File content here\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req = FakeRequest(
        method="POST",
        headers=[(b"content-type", f"multipart/form-data; boundary={boundary}".encode("latin1"))],
        body_bytes=payload,
    )

    form = await Multipart(req).form()
    assert form.field("username") == "johndoe"
    upload = form.file("file")
    assert upload is not None
    assert upload.filename() == "test.txt"
    assert await upload.read() == b"File content here"
