"""Tests for Request form parsing and request decorators."""

import pytest

from pyresponse.request import (
    Asgi,
    Authorization,
    BodyBytes,
    Fake as FakeRequest,
    FieldNotFound,
    Header,
    HeaderNotFound,
    Method,
    Multipart,
    Path,
    QueryParam,
    RequestForm,
    Sticky,
    UrlEncoded,
    WithBody,
    WithHeader,
    WithMethod,
    WithPath,
    WithQuery,
)


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

    with pytest.raises(FieldNotFound) as exc:
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


@pytest.mark.asyncio
async def test_sticky_request_body_buffering():
    messages = [
        {"type": "http.request", "body": b"hello ", "more_body": True},
        {"type": "http.request", "body": b"world", "more_body": False},
    ]

    async def mock_receive():
        return messages.pop(0)

    req = Asgi(
        scope={"type": "http", "method": "POST", "path": "/test", "headers": []},
        receive=mock_receive,
    )
    sticky_req = Sticky(req)

    # First read
    chunks1 = []
    async for chunk in sticky_req.body():
        chunks1.append(chunk)
    assert b"".join(chunks1) == b"hello world"

    # Second read from sticky cache
    chunks2 = []
    async for chunk in sticky_req.body():
        chunks2.append(chunk)
    assert b"".join(chunks2) == b"hello world"


@pytest.mark.asyncio
async def test_with_header_and_with_query_decorators():
    base = FakeRequest(
        headers=[(b"user-agent", b"pytest-test")],
        query_string=b"page=1",
    )
    enriched = WithHeader(WithQuery(base, "limit", "20"), "authorization", "Bearer secret123")

    auth = await Header(enriched, "authorization").value()
    assert auth == "Bearer secret123"
    ua = await Header(enriched, "user-agent").value()
    assert ua == "pytest-test"

    page = await QueryParam(enriched, "page").value()
    assert page == "1"
    limit = await QueryParam(enriched, "limit").value()
    assert limit == "20"


@pytest.mark.asyncio
async def test_with_method_and_with_path_decorators():
    base = FakeRequest(method="GET", path="/old")
    modified = WithPath(WithMethod(base, "DELETE"), "/new/resource")

    assert await Method(modified).as_string() == "DELETE"
    assert await Path(modified).as_string() == "/new/resource"
    assert await modified.method() == "DELETE"
    assert await modified.path() == "/new/resource"


@pytest.mark.asyncio
async def test_with_body_decorator():
    base = FakeRequest(body_bytes=b"original")
    replaced = WithBody(base, "new payload")

    chunks = [c async for c in replaced.body()]
    assert b"".join(chunks) == b"new payload"


@pytest.mark.asyncio
async def test_authorization_inspector():
    req_with_auth = FakeRequest(headers=[(b"authorization", b"Bearer token-xyz")])
    auth = Authorization(req_with_auth)
    assert await auth.has() is True
    assert await auth.value() == "Bearer token-xyz"
    assert await auth.value_or("fallback") == "Bearer token-xyz"

    req_without_auth = FakeRequest()
    auth_empty = Authorization(req_without_auth)
    assert await auth_empty.has() is False
    assert await auth_empty.value_or("fallback") == "fallback"
    with pytest.raises(HeaderNotFound):
        await auth_empty.value()


@pytest.mark.asyncio
async def test_body_bytes_decorator():
    req = FakeRequest(body_bytes=b"hello stream bytes")
    bb = BodyBytes(req)
    assert await bb.read() == b"hello stream bytes"
    assert await bb.text() == "hello stream bytes"



