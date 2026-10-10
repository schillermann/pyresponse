"""Tests for Request decorators and parsers."""

import pytest

from pyresponse.request import (
    Fake as FakeRequest,
    FieldNotFound,
    Form,
    Head,
    Header,
    HeaderNotFound,
    Json,
    Method,
    Multipart,
    ParamNotFound,
    Path,
    PathParam,
    PathParams,
    QueryParam,
    QueryParams,
    UploadFile,
    UploadNotFound,
)






@pytest.mark.asyncio
async def test_request_method_and_path():
    req = FakeRequest(method="POST", path="/api/v1/items")
    assert await Method(req).as_string() == "POST"
    assert await Path(req).as_string() == "/api/v1/items"


@pytest.mark.asyncio
async def test_request_header():
    req = FakeRequest(headers=[(b"authorization", b"Bearer token123"), (b"accept", b"application/json")])
    assert await Header(req, "Authorization").value() == "Bearer token123"
    assert await Header(req, "Accept").value() == "application/json"
    assert await Header(req, "Accept").has() is True
    assert await Header(req, "X-Missing").has() is False


    # Direct access through Headers collection
    headers = await req.head()
    assert headers.value("Authorization") == "Bearer token123"

    # Missing header without default fails fast with HeaderNotFound
    with pytest.raises(HeaderNotFound):
        await Header(req, "X-Missing").value()

    # Missing header with default returns fallback value
    assert await Header(req, "X-Missing").value(default="fallback") == "fallback"
    assert await Header(req, "X-Missing").value_or("fallback") == "fallback"



@pytest.mark.asyncio
async def test_request_query_params():
    req = FakeRequest(query_string=b"page=2&filter=active&tags=python&tags=oop")
    query = QueryParams(req)
    assert await query.param("page") == "2"
    assert await query.param("filter") == "active"
    assert await query.has("page") is True
    assert await query.has("missing") is False
    assert await query.param("missing", default="default_val") == "default_val"
    assert await query.param_or("missing", fallback="fallback_val") == "fallback_val"
    assert await query.param_list("tags") == ["python", "oop"]

    # Test single-parameter QueryParam inspector
    assert await QueryParam(req, "page").value() == "2"
    assert await QueryParam(req, "page").has() is True
    assert await QueryParam(req, "missing").has() is False
    assert await QueryParam(req, "missing").value_or("default_val") == "default_val"
    assert await QueryParam(req, "tags").values() == ["python", "oop"]

    with pytest.raises(ParamNotFound) as exc:
        await QueryParam(req, "missing").value()
    assert exc.value.name() == "missing"

    with pytest.raises(ParamNotFound) as exc:
        await query.param("missing")
    assert exc.value.name() == "missing"


@pytest.mark.asyncio
async def test_request_path_params():
    req = FakeRequest(path="/users/42/posts/100")
    path_params = PathParams(req, pattern=r"^/users/(?P<user_id>\d+)/posts/(?P<post_id>\d+)$")
    params = await path_params.params()
    assert params == {"user_id": "42", "post_id": "100"}
    assert await path_params.has("user_id") is True
    assert await path_params.has("missing") is False
    assert await path_params.param("user_id") == "42"
    assert await path_params.param("post_id") == "100"
    assert await path_params.param("missing", default="default_val") == "default_val"
    assert await path_params.param_or("missing", fallback="fallback_val") == "fallback_val"

    # Test single-parameter PathParam inspector
    pattern = r"^/users/(?P<user_id>\d+)/posts/(?P<post_id>\d+)$"
    assert await PathParam(req, "user_id", pattern=pattern).value() == "42"
    assert await PathParam(req, "user_id", pattern=pattern).has() is True
    assert await PathParam(req, "missing", pattern=pattern).has() is False
    assert await PathParam(req, "missing", pattern=pattern).value_or("fallback") == "fallback"

    with pytest.raises(ParamNotFound) as exc:
        await PathParam(req, "missing", pattern=pattern).value()
    assert exc.value.name() == "missing"

    with pytest.raises(ParamNotFound) as exc:
        await path_params.param("missing")
    assert exc.value.name() == "missing"




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

    multipart = Multipart(req)
    form = await multipart.form()
    files = await multipart.files()

    assert form.field("username") == "johndoe"
    assert form.has("username") is True
    assert form.has("missing_field") is False
    assert files.has("file") is True
    assert files.has("missing_file") is False

    upload = files.file("file")
    assert upload.filename() == "test.txt"
    assert upload.content_type() == "text/plain"
    assert await upload.read() == b"File content here"
    assert upload.head().value("content-type") == "text/plain"

    # Missing field/file with fallback returns fallback
    assert form.field_or("missing_field", fallback="fallback_val") == "fallback_val"
    fake_file = UploadFile("default.txt", "text/plain", b"default")
    assert files.file_or("missing_file", fallback=fake_file).filename() == "default.txt"

    # Missing field/file without default fails fast with FieldNotFound and UploadNotFound
    with pytest.raises(FieldNotFound) as exc_field:
        form.field("missing_field")

    assert exc_field.value.name() == "missing_field"
    assert isinstance(exc_field.value, ParamNotFound)

    with pytest.raises(UploadNotFound) as exc_file:
        files.file("missing_file")
    assert exc_file.value.name() == "missing_file"
    assert isinstance(exc_file.value, ParamNotFound)




