"""Tests for Trap and Catch exception handling decorators."""

import pytest
from httpx import ASGITransport, AsyncClient

from pyresponse import (
    BadRequest,
    Created,
    HeaderNotFoundError,
    NotFound,
    OK,
    ParamNotFoundError,
    Server,
    ServerError,
)
from pyresponse.fork import Catch, Fork, Get, Post, Trap
from pyresponse.request import Header as RequestHeader
from pyresponse.response import Body, Json


@pytest.mark.asyncio
async def test_trap_specific_exception():
    async def risky_endpoint(req):
        token = await RequestHeader(req, "Authorization").value()
        return OK(Json({"token": token}))


    app = Trap(
        Get("/secure", risky_endpoint),
        {
            HeaderNotFoundError: lambda exc, req: BadRequest(
                Json({"error": f"Missing header: {exc.name()}"})
            ),
        },
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        # Without header -> caught by Trap -> 400 Bad Request
        res_fail = await client.get("/secure")
        assert res_fail.status_code == 400
        assert res_fail.json() == {"error": "Missing header: Authorization"}

        # With header -> 200 OK
        res_ok = await client.get("/secure", headers={"Authorization": "Bearer 123"})
        assert res_ok.status_code == 200
        assert res_ok.json() == {"token": "Bearer 123"}


@pytest.mark.asyncio
async def test_trap_with_fallback():
    async def error_endpoint(req):
        raise ValueError("Something unexpected went wrong")

    app = Trap(
        Get("/error", error_endpoint),
        {
            ParamNotFoundError: lambda exc, req: NotFound(Json({"error": "Param missing"})),
        },
        fallback=lambda exc, req: ServerError(Json({"error": "Server error", "detail": str(exc)})),
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res = await client.get("/error")
        assert res.status_code == 500
        assert res.json() == {"error": "Server error", "detail": "Something unexpected went wrong"}


@pytest.mark.asyncio
async def test_catch_alias_and_composite_fork():
    app = Catch(
        Fork(
            Get("/item", lambda req: OK(Body("item ok"))),
            Post("/item", lambda req: (_ for _ in ()).throw(KeyError("missing_key"))),
        ),
        {
            KeyError: lambda exc, req: BadRequest(Json({"error": "Invalid key"})),
        },
    )

    server = Server(app)
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        res_get = await client.get("/item")
        assert res_get.status_code == 200
        assert res_get.text == "item ok"

        res_post = await client.post("/item")
        assert res_post.status_code == 400
        assert res_post.json() == {"error": "Invalid key"}
