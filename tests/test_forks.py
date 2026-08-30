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
    from pyresponse.fork import Adapted, Fixed
    from pyresponse.request import Fake as FakeRequest

    fixed_res = Ok(Body("fixed direct response"))
    fixed_endpoint = Fixed(fixed_res)
    assert fixed_endpoint.matched() is True

    req = FakeRequest()
    res = await fixed_endpoint.response(req)
    assert res == fixed_res

    # Adapted converting Response directly to Fixed
    adapted = Adapted(fixed_res)
    assert isinstance(adapted.value(), Fixed)
    assert await adapted.response(req) == fixed_res



