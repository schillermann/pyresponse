"""Tests for Fork and routing."""

import pytest
from httpx import ASGITransport, AsyncClient

from pyresponse import Ok, Server
from pyresponse.fork import Fork, Method, Path, Regex
from pyresponse.response import Body, Json


@pytest.mark.asyncio
async def test_composite_fork_path():
    app = Fork(
        Path("/hello", lambda req: Ok(Body("Hello World"))),
        Path("/about", lambda req: Ok(Body("About Us"))),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res1 = await client.get("/hello")
        assert res1.status_code == 200
        assert res1.text == "Hello World"

        res2 = await client.get("/about")
        assert res2.status_code == 200
        assert res2.text == "About Us"

        res3 = await client.get("/not-found")
        assert res3.status_code == 404


@pytest.mark.asyncio
async def test_fork_regex_with_params():
    async def user_endpoint(req):
        params = await req.path_params()
        return Ok(Json({"user_id": params.get("user_id")}))

    app = Fork(
        Regex(r"^/users/(?P<user_id>\d+)$", user_endpoint)
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res = await client.get("/users/123")
        assert res.status_code == 200
        assert res.json() == {"user_id": "123"}


@pytest.mark.asyncio
async def test_fork_method():
    app = Fork(
        Method("GET", lambda req: Ok(Body("got get"))),
        Method("POST", lambda req: Ok(Body("got post"))),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res_get = await client.get("/")
        assert res_get.status_code == 200
        assert res_get.text == "got get"

        res_post = await client.post("/")
        assert res_post.status_code == 200
        assert res_post.text == "got post"


@pytest.mark.asyncio
async def test_fallback_fork():
    from pyresponse.fork import Fallback

    app = Fallback(
        Path("/match", lambda req: Ok(Body("matched!"))),
        fallback=lambda req: Ok(Body("custom fallback!")),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res_matched = await client.get("/match")
        assert res_matched.status_code == 200
        assert res_matched.text == "matched!"

        res_fallback = await client.get("/other")
        assert res_fallback.status_code == 200
        assert res_fallback.text == "custom fallback!"


@pytest.mark.asyncio
async def test_fixed_endpoint():
    from pyresponse.fork import ConstantEndpoint, SourceEndpoint
    from pyresponse.request import Fake as FakeRequest

    fixed_res = Ok(Body("fixed direct response"))
    fixed_endpoint = ConstantEndpoint(fixed_res)
    assert fixed_endpoint.matched() is True

    req = FakeRequest()
    res = await fixed_endpoint.response(req)
    assert res == fixed_res

    # SourceEndpoint adapting Response directly as an Endpoint
    source_endpoint = SourceEndpoint(fixed_res)
    assert source_endpoint.value().matched() is True
    assert await source_endpoint.response(req) == fixed_res


@pytest.mark.asyncio
async def test_function_and_missing_endpoints():
    from pyresponse.fork.function_endpoint import FunctionEndpoint
    from pyresponse.fork.missing_endpoint import MissingEndpoint
    from pyresponse.request import Fake as FakeRequest

    fn = FunctionEndpoint(lambda req: Ok(Body("from func")))
    assert fn.matched() is True
    req = FakeRequest()
    res = await fn.response(req)
    chunks = [c async for c in res.body()]
    assert b"".join(chunks) == b"from func"

    missing = MissingEndpoint()
    assert missing.matched() is False
    with pytest.raises(Exception):
        await missing.response(req)
