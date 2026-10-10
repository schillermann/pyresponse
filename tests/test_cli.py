import pytest
from pyresponse.cli.command import UnknownCommand
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.fork import ForkCli
from pyresponse.cli.serve import ServeCommand
from pyresponse.cli.routes import RoutesInspector, RoutesTable, RoutesCommand
from pyresponse.cli.app import CliApp
from pyresponse.fork.fork import Fork
from pyresponse.fork.get import Get
from pyresponse.fork.post import Post
from pyresponse.fork.prefix import Prefix
from pyresponse.request.request import Request
from pyresponse.response.response import Response
from pyresponse.response.text import Text


class DummyEndpoint:
    def matched(self) -> bool:
        return True

    async def route(self, req: Request) -> "DummyEndpoint":
        return self

    async def response(self, req: Request) -> Response:
        return Text("dummy")


def test_help_command() -> None:
    cmd = HelpCommand()
    assert cmd.name() == "help"
    assert cmd.matches("help") is True
    assert cmd.matches("-h") is True
    assert cmd.matches("other") is False
    assert cmd.execute([]) == 0


def test_unknown_command(capsys: pytest.CaptureFixture[str]) -> None:
    cmd = UnknownCommand("foobar")
    assert cmd.name() == "foobar"
    assert cmd.matches("foobar") is False
    assert cmd.execute([]) == 1
    assert "Unknown command: 'foobar'" in capsys.readouterr().out


def test_fork_cli_routing() -> None:
    calls = []

    class PingCommand:
        def name(self) -> str:
            return "ping"

        def description(self) -> str:
            return "ping command"

        def matches(self, verb: str) -> bool:
            return verb == "ping"

        def execute(self, args: list[str]) -> int:
            calls.append(args)
            return 0

    fork = ForkCli([PingCommand()])
    assert fork.execute(["ping", "arg1"]) == 0
    assert calls == [["arg1"]]
    assert fork.execute(["unknown"]) == 1
    assert fork.execute([]) == 0


def test_serve_command_matching() -> None:
    serve = ServeCommand("app:portal", "127.0.0.1", 9000, reload=False)
    assert serve.name() == "serve"
    assert serve.matches("serve") is True
    assert serve.matches("server") is True
    assert serve.matches("start") is True
    assert serve.matches("routes") is False


def test_routes_inspector_and_table() -> None:
    routes = Fork(
        Prefix("/api", Fork(
            Get(DummyEndpoint()),
            Post(DummyEndpoint()),
        )),
        Get(DummyEndpoint()),
    )
    entries = RoutesInspector(routes).entries()
    assert len(entries) >= 2
    methods = [e.method() for e in entries]
    assert "GET" in methods
    assert "POST" in methods

    table = RoutesTable(entries)
    text = str(table)
    assert "METHOD" in text
    assert "PATH" in text
    assert "Total:" in text


def test_routes_command(capsys: pytest.CaptureFixture[str]) -> None:
    routes = Fork(Get(DummyEndpoint()))
    cmd = RoutesCommand(routes)
    assert cmd.name() == "routes"
    assert cmd.matches("routes") is True
    assert cmd.matches("route:list") is True
    assert cmd.execute([]) == 0
    assert "GET" in capsys.readouterr().out


def test_cli_app_help(capsys: pytest.CaptureFixture[str]) -> None:
    app = CliApp()
    assert app.execute(["help"]) == 0
    out = capsys.readouterr().out
    assert "PyResponse Developer Console" in out
    assert "serve" in out
