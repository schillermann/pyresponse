"""Tests for Request decorators and parsers."""

import pytest

from pyresponse.request import (
    AsgiRequest,
    Fake as FakeRequest,
    FieldNotFoundError,
    Form,
    Head,
    Header,
    HeaderNotFoundError,
    Json,
    Method,
    Multipart,
    ParamNotFoundError,
    Path,
    PathParam,
    PathParams,
    QueryParam,
    QueryParams,
    RequestForm,
    UploadFile,
    UploadNotFoundError,
    UrlEncoded,
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
    assert await Header(req, "Accept").as_string() == "application/json"
    assert await Header(req, "Accept").has() is True
    assert await Header(req, "X-Missing").has() is False


    # Direct access through Headers collection
    headers = await req.head()
    assert headers.value("Authorization") == "Bearer token123"

    # Missing header without default fails fast with HeaderNotFoundError
    with pytest.raises(HeaderNotFoundError):
        await Header(req, "X-Missing").value()

    # Missing header with default returns fallback value
    assert await Header(req, "X-Missing").as_string(default="fallback") == "fallback"
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

    with pytest.raises(ParamNotFoundError) as exc:
        await QueryParam(req, "missing").value()
    assert exc.value.name() == "missing"

    with pytest.raises(ParamNotFoundError) as exc:
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

    with pytest.raises(ParamNotFoundError) as exc:
        await PathParam(req, "missing", pattern=pattern).value()
    assert exc.value.name() == "missing"

    with pytest.raises(ParamNotFoundError) as exc:
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

    # Missing field/file without default fails fast with FieldNotFoundError and UploadNotFoundError
    with pytest.raises(FieldNotFoundError) as exc_field:
        form.field("missing_field")

    assert exc_field.value.name() == "missing_field"
    assert isinstance(exc_field.value, ParamNotFoundError)

    with pytest.raises(UploadNotFoundError) as exc_file:
        files.file("missing_file")
    assert exc_file.value.name() == "missing_file"
    assert isinstance(exc_file.value, ParamNotFoundError)



@pytest.mark.asyncio
async def test_request_urlencoded():
    payload = b"username=johndoe&email=john%40example.com&tag=python&tag=oop"
    req = FakeRequest(
        method="POST",
        headers=[(b"content-type", b"application/x-www-form-urlencoded")],
        body_bytes=payload,
    )

    url_encoded = UrlEncoded(req)
    assert await url_encoded.field("username") == "johndoe"
    assert await url_encoded.field("email") == "john@example.com"
    assert await url_encoded.has("username") is True
    assert await url_encoded.has("missing") is False
    assert await url_encoded.field_or("missing", fallback="fallback_val") == "fallback_val"

    form = await url_encoded.form()
    assert form.field("username") == "johndoe"
    assert form.field_list("tag") == ["python", "oop"]
    assert form.field_or("missing", fallback="fallback_val") == "fallback_val"

    with pytest.raises(FieldNotFoundError) as exc:
        await url_encoded.field("missing")
    assert exc.value.name() == "missing"


@pytest.mark.asyncio
async def test_request_form_unified_urlencoded_and_multipart():
    # 1. URL-Encoded via unified RequestForm
    req_urlencoded = FakeRequest(
        method="POST",
        headers=[(b"content-type", b"application/x-www-form-urlencoded")],
        body_bytes=b"title=Article+Title&status=draft",
    )
    form1 = RequestForm(req_urlencoded)
    assert await form1.field("title") == "Article Title"
    assert await form1.has("title") is True
    assert await form1.has("missing") is False
    assert await form1.has_file("any_file") is False
    parsed_form = await form1.form()
    assert parsed_form.field("status") == "draft"


    # 2. Multipart via unified RequestForm
    boundary = "----TestBoundary123"
    payload = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="title"\r\n\r\n'
        f"Multipart Title\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="avatar"; filename="avatar.png"\r\n'
        f"Content-Type: image/png\r\n\r\n"
        f"PNGDATA\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req_multipart = FakeRequest(
        method="POST",
        headers=[(b"content-type", f"multipart/form-data; boundary={boundary}".encode("latin1"))],
        body_bytes=payload,
    )
    form2 = RequestForm(req_multipart)
    assert await form2.field("title") == "Multipart Title"
    assert await form2.has("title") is True
    assert await form2.has_file("avatar") is True
    avatar = await form2.file("avatar")
    assert avatar.filename() == "avatar.png"
    assert avatar.content_type() == "image/png"
    assert await avatar.read() == b"PNGDATA"

    # Direct Multipart helpers
    mp = Multipart(req_multipart)
    assert await mp.field("title") == "Multipart Title"
    assert await mp.has("title") is True
    assert await mp.has_file("avatar") is True
    mp_file = await mp.file("avatar")
    assert mp_file.filename() == "avatar.png"



