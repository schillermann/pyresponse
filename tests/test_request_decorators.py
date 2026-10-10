"""Tests for Request inspectors, CLI output decorators, and command envelopes."""

import pytest
from pyresponse.cli import (
    Arguments,
    CliCommand,
    ColorOutput,
    CommandEnvelope,
    ExitCode,
    MemoryOutput,
    OutputEnvelope,
    PrefixedOutput,
    SilentOutput,
)
from pyresponse.request import (
    Accept,
    BasicAuth,
    BearerToken,
    ContentType,
    Fake as FakeReq,
    Host,
    Json,
    QueryParams,
    UserAgent,
    WithAccept,
    WithBasicAuth,
    WithBearerToken,
    WithHeader,
    WithJsonBody,
    WithQueryParam,
    WithUserAgent,
    WithoutHeader,
    WithoutQueryParam,
)


def test_cli_output_decorators():
    mem = MemoryOutput()
    env = OutputEnvelope(mem)
    env.print("base message")
    env.error("base error")
    assert mem.stdout() == "base message"
    assert mem.stderr() == "base error"

    mem_prefixed = MemoryOutput()
    prefixed = PrefixedOutput(mem_prefixed, prefix="[pyr] ")
    prefixed.print("hello")
    prefixed.error("fail")
    assert mem_prefixed.stdout() == "[pyr] hello"
    assert mem_prefixed.stderr() == "[pyr] fail"

    silent = SilentOutput()
    silent.print("ignored")
    silent.error("ignored")


def test_command_envelope():
    calls = []

    class InnerCmd(CliCommand):
        def name(self) -> str:
            return "inner"

        def description(self) -> str:
            return "Inner command description"

        def matches(self, verb: str) -> bool:
            return verb == "inner"

        def execute(self, args: Arguments) -> ExitCode:
            calls.append(args)
            return ExitCode(42)

    cmd = CommandEnvelope(InnerCmd())
    assert cmd.name() == "inner"
    assert cmd.description() == "Inner command description"
    assert cmd.matches("inner") is True
    assert cmd.matches("other") is False
    assert cmd.execute(Arguments("arg1", "arg2")) == ExitCode(42)
    assert calls == [Arguments("arg1", "arg2")]


def test_color_output_decorator():
    mem = MemoryOutput()
    colored = ColorOutput(mem)
    colored.print("success")
    colored.error("failure")

    assert "\033[32msuccess\033[0m" in mem.stdout()
    assert "\033[31mfailure\033[0m" in mem.stderr()


@pytest.mark.asyncio
async def test_request_auth_and_body_decorators():
    base = FakeReq(method="GET", path="/")

    bearer_req = WithBearerToken(base, "my-jwt-token")
    bearer = BearerToken(bearer_req)
    assert await bearer.has() is True
    assert await bearer.token() == "my-jwt-token"

    basic_req = WithBasicAuth(base, "admin", "secret123")
    basic = BasicAuth(basic_req)
    assert await basic.has() is True
    assert await basic.username() == "admin"
    assert await basic.password() == "secret123"

    json_req = WithJsonBody(base, {"greeting": "hello", "count": 3})
    json_inspector = Json(json_req)
    assert await json_inspector.content() == {"greeting": "hello", "count": 3}
    assert (await json_req.head()).value("content-type") == "application/json"

    stripped_req = WithoutHeader(json_req, "content-type")
    assert (await stripped_req.head()).has("content-type") is False


@pytest.mark.asyncio
async def test_request_query_param_decorators():
    req = FakeReq(method="GET", path="/search", query_string=b"q=books&sort=asc")

    paged_req = WithQueryParam(req, "page", "2")
    qp = QueryParams(paged_req)
    assert await qp.param("page") == "2"
    assert await qp.param("q") == "books"

    desc_req = WithQueryParam(paged_req, "sort", "desc")
    qp_desc = QueryParams(desc_req)
    assert await qp_desc.param("sort") == "desc"

    clean_req = WithoutQueryParam(desc_req, "sort")
    qp_clean = QueryParams(clean_req)
    assert await qp_clean.has("sort") is False
    assert await qp_clean.has("q") is True


@pytest.mark.asyncio
async def test_request_header_domain_decorators():
    base = FakeReq(method="GET", path="/")

    ct_req = WithHeader(base, "Content-Type", "application/json; charset=utf-8")
    ct_inspector = ContentType(ct_req)
    assert await ct_inspector.value() == "application/json; charset=utf-8"
    assert await ct_inspector.mime_type() == "application/json"
    assert await ct_inspector.has() is True

    ua_req = WithUserAgent(base, "Mozilla/5.0 PyResponse")
    ua_inspector = UserAgent(ua_req)
    assert await ua_inspector.value() == "Mozilla/5.0 PyResponse"
    assert await ua_inspector.has() is True

    acc_req = WithAccept(base, "text/html,application/xhtml+xml")
    acc_inspector = Accept(acc_req)
    assert await acc_inspector.value() == "text/html,application/xhtml+xml"
    assert await acc_inspector.has() is True

    host_req = WithHeader(base, "Host", "api.example.com:8080")
    host_inspector = Host(host_req)
    assert await host_inspector.value() == "api.example.com:8080"
    assert await host_inspector.hostname() == "api.example.com"
