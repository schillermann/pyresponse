"""Tests for Server and AsgiApp integration."""

import pytest
from httpx import ASGITransport, AsyncClient

from pyresponse import (
    Ok,
    AsgiApp,
    Fake,
    Server,
    StatusLine,
)
from pyresponse.response import Body, Header


@pytest.mark.asyncio
async def test_server_with_custom_endpoint_class():
    class GreetingEndpoint:
        def response(self, request):
            return Ok(Body("Hello from endpoint class"))

    server = Server(GreetingEndpoint())
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.text == "Hello from endpoint class"


@pytest.mark.asyncio
async def test_server_async_callable_handler():
    async def async_handler(request):
        return StatusLine(
            Header(
                Body('{"message": "async ok"}'),
                "Content-Type",
                "application/json",
            ),
            status=200,
        )

    server = Server(async_handler)
    async with AsyncClient(transport=ASGITransport(app=server.app()), base_url="http://testserver") as client:
        response = await client.post("/test")
        assert response.status_code == 200
        assert response.json() == {"message": "async ok"}


@pytest.mark.asyncio
async def test_lifespan_lifecycle():
    lifespan = Fake()
    app = AsgiApp(lambda req: Ok(Body("ok")), lifespan=lifespan)

    # Simulate lifespan startup
    startup_messages = []

    async def receive_startup():
        return {"type": "lifespan.startup"}

    async def send_startup(msg):
        startup_messages.append(msg)

    # Run lifespan startup scope
    scope = {"type": "lifespan"}

    # We test via async task or directly
    # Since lifespan loop runs until shutdown, let's run startup then shutdown
    events = [{"type": "lifespan.startup"}, {"type": "lifespan.shutdown"}]
    sent = []

    async def mock_receive():
        return events.pop(0)

    async def mock_send(msg):
        sent.append(msg)

    await app(scope, mock_receive, mock_send)

    assert lifespan.started() is True
    assert lifespan.stopped() is True

    assert sent == [
        {"type": "lifespan.startup.complete"},
        {"type": "lifespan.shutdown.complete"},
    ]


@pytest.mark.asyncio
async def test_asgi_decorators():
    from pyresponse.asgi import AsgiEnvelope, AsgiHttpApp, LoggedAsgi, WithLifespan
    from pyresponse.cli import MemoryOutput

    http_app = AsgiHttpApp(lambda req: Ok(Body("raw asgi")))
    assert len(http_app.routes()) == 1

    # AsgiEnvelope
    env = AsgiEnvelope(http_app)

    # LoggedAsgi
    mem = MemoryOutput()
    logged = LoggedAsgi(env, output=mem)

    async with AsyncClient(transport=ASGITransport(app=logged), base_url="http://testserver") as client:
        res = await client.get("/hello-asgi")
        assert res.status_code == 200
        assert res.text == "raw asgi"

    assert "GET /hello-asgi -> 200" in mem.stdout()

    # WithLifespan
    lifespan = Fake()
    with_ls = WithLifespan(http_app, lifespan=lifespan)
    events = [{"type": "lifespan.startup"}, {"type": "lifespan.shutdown"}]
    sent = []

    async def mock_ls_receive():
        return events.pop(0)

    async def mock_ls_send(msg):
        sent.append(msg)

    await with_ls(
        {"type": "lifespan"},
        mock_ls_receive,
        mock_ls_send,
    )
    assert lifespan.started() is True
    assert lifespan.stopped() is True


