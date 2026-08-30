"""Tests for HTTP method routing forks."""

import pytest
from httpx import ASGITransport, AsyncClient

from pyresponse import OK, Server
from pyresponse.fork import (
    Delete,
    Fork,
    Get,
    Head,
    Options,
    Patch,
    Path,
    Post,
    Put,
)
from pyresponse.response import Body, Header


@pytest.mark.asyncio
async def test_all_http_methods_with_paths():
    app = Fork(
        Get("/resource", lambda req: OK(Body("got get"))),
        Post("/resource", lambda req: OK(Body("got post"))),
        Put("/resource", lambda req: OK(Body("got put"))),
        Delete("/resource", lambda req: OK(Body("got delete"))),
        Patch("/resource", lambda req: OK(Body("got patch"))),
        Options("/resource", lambda req: OK(Header(Body(""), "Allow", "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD"))),
        Head("/resource", lambda req: OK(Body(""))),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res_get = await client.get("/resource")
        assert res_get.status_code == 200
        assert res_get.text == "got get"

        res_post = await client.post("/resource")
        assert res_post.status_code == 200
        assert res_post.text == "got post"

        res_put = await client.put("/resource")
        assert res_put.status_code == 200
        assert res_put.text == "got put"

        res_delete = await client.delete("/resource")
        assert res_delete.status_code == 200
        assert res_delete.text == "got delete"

        res_patch = await client.patch("/resource")
        assert res_patch.status_code == 200
        assert res_patch.text == "got patch"

        res_options = await client.options("/resource")
        assert res_options.status_code == 200
        assert res_options.headers.get("allow") == "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD"

        res_head = await client.head("/resource")
        assert res_head.status_code == 200


@pytest.mark.asyncio
async def test_method_fork_single_argument():
    app = Path(
        "/single",
        Fork(
            Get(lambda req: OK(Body("get on single"))),
            Post(lambda req: OK(Body("post on single"))),
        ),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res1 = await client.get("/single")
        assert res1.status_code == 200
        assert res1.text == "get on single"

        res2 = await client.post("/single")
        assert res2.status_code == 200
        assert res2.text == "post on single"

        res3 = await client.put("/single")
        assert res3.status_code == 404


@pytest.mark.asyncio
async def test_generic_method_fork():
    from pyresponse.fork import Method

    app = Fork(
        Method("GET", lambda req: OK(Body("generic get"))),
        Method("POST", lambda req: OK(Body("generic post"))),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res1 = await client.get("/")
        assert res1.status_code == 200
        assert res1.text == "generic get"

        res2 = await client.post("/")
        assert res2.status_code == 200
        assert res2.text == "generic post"

        res3 = await client.delete("/")
        assert res3.status_code == 404

