"""Tests for routing and fork decorators."""

import pytest
from pyresponse.cli.output import MemoryOutput
from pyresponse.fork import (
    BranchEnvelope,
    ConstantEndpoint,
    Envelope as EndpointEnvelope,
    Fork,
    ForkEnvelope,
    Get,
    GuardedBranch,
    GuardedEndpoint,
    HeaderFork,
    Host,
    LoggedFork,
    MeasuredEndpoint,
    Route,
    TransformedEndpoint,
)
from pyresponse.request import Fake as FakeRequest, WithHeader
from pyresponse.response import BytesBody, Header, Ok, StreamBody, Text, TextBody


@pytest.mark.asyncio
async def test_endpoint_decorators():
    base_endpoint = ConstantEndpoint(Ok(Text("endpoint response")))
    env = EndpointEnvelope(base_endpoint)
    assert env.matched() is True

    req = FakeRequest(method="GET", path="/test")
    res = await env.response(req)
    chunks = [c async for c in res.body()]
    assert b"".join(chunks) == b"endpoint response"

    # GuardedEndpoint: rejected
    guarded_no = GuardedEndpoint(base_endpoint, guard=lambda r: False)
    res_rejected = await guarded_no.response(req)
    assert (await res_rejected.head()).status() == 403

    # GuardedEndpoint: allowed
    guarded_yes = GuardedEndpoint(base_endpoint, guard=lambda r: True)
    res_allowed = await guarded_yes.response(req)
    assert (await res_allowed.head()).status() == 200

    # MeasuredEndpoint
    measured = MeasuredEndpoint(base_endpoint, metric="test_metric")
    res_measured = await measured.response(req)
    head_measured = await res_measured.head()
    assert head_measured.has("server-timing") is True
    assert "test_metric;dur=" in head_measured.value("server-timing")

    # TransformedEndpoint
    transformed = TransformedEndpoint(
        base_endpoint,
        transformation=lambda r: Header(r, "X-Custom-Env", "Transformed"),
    )
    res_transformed = await transformed.response(req)
    head_transformed = await res_transformed.head()
    assert head_transformed.value("x-custom-env") == "Transformed"


@pytest.mark.asyncio
async def test_branch_decorators():
    inner_branch = Get("/hello", ConstantEndpoint(Ok(Text("world"))))
    env_branch = BranchEnvelope(inner_branch)

    req_match = FakeRequest(method="GET", path="/hello")
    res_endpoint = await env_branch.route(req_match)
    assert res_endpoint.matched() is True

    guarded_true = GuardedBranch(inner_branch, lambda r: True)
    assert (await guarded_true.route(req_match)).matched() is True

    guarded_false = GuardedBranch(inner_branch, lambda r: False)
    assert (await guarded_false.route(req_match)).matched() is False


@pytest.mark.asyncio
async def test_fork_envelope_and_logging():
    base_fork = Fork(
        Get("/users", lambda r: Ok(Text("users list"))),
    )

    env = ForkEnvelope(base_fork)
    assert len(env.routes()) == 1

    mem = MemoryOutput()
    logged = LoggedFork(env, output=mem)

    req_match = FakeRequest(method="GET", path="/users")
    endpoint_match = await logged.route(req_match)
    assert endpoint_match.matched() is True
    assert "Matched route: GET /users" in mem.stdout()

    req_miss = FakeRequest(method="GET", path="/missing")
    endpoint_miss = await logged.route(req_miss)
    assert endpoint_miss.matched() is False
    assert "Unmatched route: GET /missing" in mem.stdout()


@pytest.mark.asyncio
async def test_host_and_header_forks():
    host_fork = Host("api.example.com", ConstantEndpoint(Ok(Text("api data"))))
    req_api = WithHeader(FakeRequest(method="GET"), "Host", "api.example.com")
    assert (await host_fork.route(req_api)).matched() is True

    req_other = WithHeader(FakeRequest(method="GET"), "Host", "other.example.com")
    assert (await host_fork.route(req_other)).matched() is False

    v2_fork = HeaderFork("X-API-Version", "v2", ConstantEndpoint(Ok(Text("v2 data"))))
    req_v2 = WithHeader(FakeRequest(method="GET"), "X-API-Version", "v2")
    assert (await v2_fork.route(req_v2)).matched() is True

    req_v1 = WithHeader(FakeRequest(method="GET"), "X-API-Version", "v1")
    assert (await v2_fork.route(req_v1)).matched() is False


@pytest.mark.asyncio
async def test_route_and_pure_body_objects():
    bb = BytesBody(b"raw binary data")
    assert bb.matched() is True
    assert (await bb.response(FakeRequest())) == bb
    head = await bb.head()
    assert head.status() == 200
    assert (b"content-length", b"15") in head.headers()
    body_chunks = [c async for c in bb.body()]
    assert body_chunks == [b"raw binary data"]

    tb = TextBody("hello world")
    assert tb.matched() is True
    head_t = await tb.head()
    assert (b"content-length", b"11") in head_t.headers()
    assert [c async for c in tb.body()] == [b"hello world"]

    async def sample_stream():
        yield b"chunk1"
        yield b"chunk2"

    sb = StreamBody(sample_stream())
    assert sb.matched() is True
    assert [c async for c in sb.body()] == [b"chunk1", b"chunk2"]

    route = Route("POST", "/submit", Ok(tb))
    assert len(route.routes()) == 1
    assert route.routes()[0].method() == "POST"
    assert route.routes()[0].path() == "/submit"

    req_match = FakeRequest(method="POST", path="/submit")
    endpoint = await route.route(req_match)
    assert endpoint.matched() is True
    res = await endpoint.response(req_match)
    assert [c async for c in res.body()] == [b"hello world"]

    req_wrong_method = FakeRequest(method="GET", path="/submit")
    assert (await route.route(req_wrong_method)).matched() is False

    req_wrong_path = FakeRequest(method="POST", path="/other")
    assert (await route.route(req_wrong_path)).matched() is False
