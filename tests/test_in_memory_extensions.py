"""Tests for in-memory ASGI execution, multipart request builders, body inspectors, and assertions."""

from collections.abc import Callable, MutableMapping
from typing import Any, AsyncIterator
import pytest

from pyresponse import AsgiApp, Error, fork, request, response
from pyresponse.fork import CorsEndpoint, Post, Route, Trap
from pyresponse.request import (
    BodyBytes as ReqBodyBytes, FormField, FormFile, Header, Multipart,
    PathParam, QueryParam, Request, WithBearerToken, WithHeader,
    WithJsonBody, WithMultipartBody, WithParams,
)
from pyresponse.response import (
    Asgi as AsgiResponse, AsgiNotStarted, BodyBytes, BodyJson, BodyText,
    ExpectedBody, ExpectedHeader, ExpectedJson, ExpectedStatus, Json,
    NoContent, Redirect, Response, StatusLine, Sticky, Text, Verified, WithBody,
)


class ForbiddenError(Error):
    """Domain error representing an HTTP 403 Forbidden failure."""


class CountingApp:
    """Fake ASGI 3.0 callable counting invocations and emitting multi-chunk responses."""

    def __init__(self, chunks: tuple[bytes, ...] = (b"part1-", b"part2")) -> None:
        self._chunks = chunks
        self._calls: list[int] = []

    def count(self) -> int:
        return len(self._calls)

    async def __call__(
        self, scope: MutableMapping[str, Any], receive: Callable[..., Any], send: Callable[..., Any]
    ) -> None:
        self._calls.append(1)
        await receive()
        await send({"type": "http.response.start", "status": 200, "headers": [(b"x-custom", b"ok")]})
        for idx, chunk in enumerate(self._chunks):
            await send({"type": "http.response.body", "body": chunk, "more_body": idx < len(self._chunks) - 1})


class SilentAsgiApp:
    """Fake ASGI 3.0 callable that completes without sending http.response.start."""

    async def __call__(
        self, scope: MutableMapping[str, Any], receive: Callable[..., Any], send: Callable[..., Any]
    ) -> None:
        await receive()


@pytest.mark.asyncio
async def test_asgi_response_basic_and_echo():
    res = AsgiResponse(AsgiApp(fork.Fake(Text("hi"))), request.Fake())
    assert (await res.head()).status() == 200
    assert await BodyBytes(res).bytes() == b"hi"

    async def echo_endpoint(req: Request) -> Response:
        return Json({
            "method": await req.method(),
            "path": await req.path(),
            "user_id": await QueryParam(req, "user_id").value(),
            "doc_id": await PathParam(req, "doc_id").value(),
            "auth": await Header(req, "authorization").value(),
            "body": await ReqBodyBytes(req).text(),
        })

    echo_app = AsgiApp(Post("/api/echo", echo_endpoint))
    echo_req = WithParams(
        WithBearerToken(
            WithJsonBody(
                request.Fake(method="POST", path="/api/echo", query_string=b"user_id=usr_101"),
                {"hello": "world"},
            ),
            "token_abc",
        ),
        {"doc_id": "doc_99"},
    )
    echo_res = AsgiResponse(echo_app, echo_req)
    assert (await echo_res.head()).status() == 200
    payload = await BodyJson(echo_res).value()
    assert payload == {
        "method": "POST",
        "path": "/api/echo",
        "user_id": "usr_101",
        "doc_id": "doc_99",
        "auth": "Bearer token_abc",
        "body": '{"hello": "world"}',
    }


@pytest.mark.asyncio
async def test_asgi_response_single_execution_and_multipart_chunks():
    app = CountingApp((b"hello ", b"in-memory ", b"world"))
    res = AsgiResponse(app, request.Fake())
    assert app.count() == 0
    assert (await res.head()).status() == 200
    assert app.count() == 1
    assert await BodyText(res).text() == "hello in-memory world"
    assert app.count() == 1


@pytest.mark.asyncio
async def test_asgi_response_cors_trap_redirect_and_errors():
    cors_app = AsgiApp(CorsEndpoint(fork.Fake(Text("ok")), allow_origin="https://makler.test"))
    cors_res = AsgiResponse(cors_app, request.Fake())
    assert (await cors_res.head()).value("access-control-allow-origin") == "https://makler.test"

    async def failing_endpoint(req: Request) -> Response:
        raise ForbiddenError("access denied")

    trap_app = AsgiApp(
        Trap(
            Route("GET", "/secret", failing_endpoint),
            {ForbiddenError: lambda err, req: StatusLine(Text("forbidden"), 403)},
        )
    )
    trap_res = AsgiResponse(trap_app, request.Fake(path="/secret"))
    assert (await trap_res.head()).status() == 403
    assert await BodyText(trap_res).text() == "forbidden"

    redirect_app = AsgiApp(fork.Fake(Redirect("/login", status=307)))
    redirect_res = AsgiResponse(redirect_app, request.Fake())
    assert (await redirect_res.head()).status() == 307
    assert (await redirect_res.head()).value("location") == "/login"

    unhandled_app = AsgiApp(Route("GET", "/boom", failing_endpoint))
    with pytest.raises(ForbiddenError):
        await AsgiResponse(unhandled_app, request.Fake(path="/boom")).head()

    with pytest.raises(AsgiNotStarted):
        await AsgiResponse(SilentAsgiApp(), request.Fake()).head()


@pytest.mark.asyncio
async def test_with_multipart_body_roundtrip_with_umlauts_and_binary():
    binary_data = bytes(range(256))
    base_req = WithHeader(
        request.Fake(method="POST", path="/api/documents/upload"),
        "Content-Type",
        "text/plain",
    )
    multipart_req = WithMultipartBody(
        base_req,
        [
            FormFile("file", "Grundbuch_Bonn.bin", binary_data, "application/octet-stream"),
            FormField("category", "Grundbuch Köln"),
            FormField("property_id", "p-901"),
        ],
    )
    head = await multipart_req.head()
    content_type_headers = [v for k, v in head.headers() if k.lower() == b"content-type"]
    assert len(content_type_headers) == 1

    parsed = Multipart(multipart_req)
    assert await parsed.field("category") == "Grundbuch Köln"
    assert await parsed.field("property_id") == "p-901"
    uploaded = await parsed.file("file")
    assert uploaded.filename() == "Grundbuch_Bonn.bin"
    assert uploaded.content_type() == "application/octet-stream"
    assert await uploaded.read() == binary_data


@pytest.mark.asyncio
async def test_response_body_inspectors_and_declarative_assertions():
    async def gen() -> AsyncIterator[bytes]:
        yield b'{"data": {"sender": '
        yield b'"assistant", "items": [10, 20]}}'

    streamed = Sticky(WithBody(response.Fake(status=201, headers=[(b"x-trace", b"abc-123")]), gen()))
    await Verified(
        streamed,
        ExpectedStatus(201),
        ExpectedHeader("x-trace", "abc"),
        ExpectedBody('"sender": "assistant"'),
        ExpectedJson(("data", "sender"), "assistant"),
        ExpectedJson(("data", "items", 1), 20),
    ).verify()

    empty_res = NoContent(response.Fake())
    assert await BodyBytes(empty_res).value() == b""
    assert await BodyText(empty_res).value() == ""
    with pytest.raises(ValueError):
        await BodyJson(empty_res).value()

    with pytest.raises(AssertionError):
        await ExpectedStatus(200).verify(streamed)

    lazy_req = WithJsonBody(request.Fake(), object())
    with pytest.raises(TypeError):
        _ = [chunk async for chunk in lazy_req.body()]
