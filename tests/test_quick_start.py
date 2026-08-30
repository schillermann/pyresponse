"""Test for Quick Start example from README.md."""

import pytest
from httpx import ASGITransport, AsyncClient

from pyresponse import Server
from pyresponse.response import Ok, Body, Header


@pytest.mark.asyncio
async def test_quick_start_example():
    server = Server(
        lambda request: (
            Ok(
                Header(
                    Body("<h1>Hello from PyResponse!</h1>"),
                    "Content-Type",
                    "text/html",
                )
            )
        ),
        port=8000,
    )

    app = server.app()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html"
        assert response.text == "<h1>Hello from PyResponse!</h1>"
