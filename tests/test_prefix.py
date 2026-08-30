"""Tests for Prefix routing fork."""

import pytest
from httpx import ASGITransport, AsyncClient

from pyresponse import OK, Server
from pyresponse.fork import Fork, Get, Path, Post, Prefix
from pyresponse.response import Body, Json


@pytest.mark.asyncio
async def test_prefix_routing():
    app = Prefix(
        "/api/v1",
        Fork(
            Get("/users", lambda req: OK(Json({"users": ["Alice", "Bob"]}))),
            Post("/users", lambda req: OK(Json({"created": True}))),
            Get("/status", lambda req: OK(Body("API OK"))),
        ),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res1 = await client.get("/api/v1/users")
        assert res1.status_code == 200
        assert res1.json() == {"users": ["Alice", "Bob"]}

        res2 = await client.post("/api/v1/users")
        assert res2.status_code == 200
        assert res2.json() == {"created": True}

        res3 = await client.get("/api/v1/status")
        assert res3.status_code == 200
        assert res3.text == "API OK"

        # Not matching prefix
        res4 = await client.get("/other/users")
        assert res4.status_code == 404

        # Non-boundary prefix mismatch (e.g. /api/v10)
        res5 = await client.get("/api/v10/users")
        assert res5.status_code == 404


@pytest.mark.asyncio
async def test_nested_prefixes():
    app = Prefix(
        "/api",
        Fork(
            Prefix(
                "/v1",
                Fork(
                    Get("/hello", lambda req: OK(Body("Hello v1"))),
                ),
            ),
            Prefix(
                "/v2",
                Fork(
                    Get("/hello", lambda req: OK(Body("Hello v2"))),
                ),
            ),
        ),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res_v1 = await client.get("/api/v1/hello")
        assert res_v1.status_code == 200
        assert res_v1.text == "Hello v1"

        res_v2 = await client.get("/api/v2/hello")
        assert res_v2.status_code == 200
        assert res_v2.text == "Hello v2"


@pytest.mark.asyncio
async def test_prefix_with_root_path():
    app = Prefix(
        "/api",
        Path("/", lambda req: OK(Body("API root"))),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res1 = await client.get("/api")
        assert res1.status_code == 200
        assert res1.text == "API root"

        res2 = await client.get("/api/")
        assert res2.status_code == 200
        assert res2.text == "API root"
