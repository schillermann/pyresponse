import pytest
from pyresponse.cli.app import CliApp
from pyresponse.cli.command import UnknownCommand
from pyresponse.cli.fork import ForkCli
from pyresponse.cli.help import HelpCommand
from pyresponse.cli.output import ConsoleOutput, MemoryOutput
from pyresponse.cli.routes import RouteEntry, RoutesCommand, RoutesTable, SourceRoutes, TableRow
from pyresponse.cli.serve import ServeCommand
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
            calls.append("ping")
            return 0

    cli = ForkCli([PingCommand()])
    assert cli.execute(["ping"]) == 0
    assert calls == ["ping"]
    assert cli.execute(["pong"]) == 1


def test_alias_command() -> None:
    from pyresponse.cli.alias import AliasCommand

    calls = []

    class BaseCommand:
        def name(self) -> str:
            return "status"

        def description(self) -> str:
            return "Status command"

        def matches(self, verb: str) -> bool:
            return verb == "status"

        def execute(self, args: list[str]) -> int:
            calls.append(args)
            return 0

    cmd = AliasCommand(BaseCommand(), "st", "stat")
    assert cmd.name() == "status"
    assert cmd.description() == "Status command"
    assert cmd.matches("status") is True
    assert cmd.matches("st") is True
    assert cmd.matches("stat") is True
    assert cmd.matches("other") is False
    assert cmd.execute(["--json"]) == 0
    assert calls == [["--json"]]


def test_routes_inspector_and_table() -> None:
    routes = Fork(
        Prefix("/api", Fork(
            Get("/users", DummyEndpoint()),
            Post("/users", DummyEndpoint()),
        )),
        Get(DummyEndpoint()),
    )
    entries = SourceRoutes(routes).entries()
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


def test_routes_command_with_memory_output() -> None:
    routes = Fork(Get(DummyEndpoint()))
    mem = MemoryOutput()
    cmd = RoutesCommand(routes, output=mem)
    assert cmd.execute([]) == 0
    assert "GET" in mem.stdout()
    assert mem.stderr() == ""


def test_cli_app_help(capsys: pytest.CaptureFixture[str]) -> None:
    app = CliApp()
    assert app.execute(["help"]) == 0
    out = capsys.readouterr().out
    assert "PyResponse Developer Console" in out
    assert "serve" in out


def test_pyresponse_main_entrypoint() -> None:
    import pyresponse.__main__

    assert pyresponse.__main__.main(["help"]) == 0


def test_pyr_main_entrypoint() -> None:
    import pyr.__main__

    assert pyr.__main__.main(["help"]) == 0


def test_routes_command_missing_target(capsys: pytest.CaptureFixture[str]) -> None:
    cmd = RoutesCommand()
    assert cmd.execute(["nonexistent_module_xyz:app"]) == 1
    err = capsys.readouterr().err
    assert "Cannot import module" in err or "Could not load" in err


def test_routes_command_auto_discovery(capsys: pytest.CaptureFixture[str]) -> None:
    cmd = RoutesCommand()
    assert cmd.execute([]) == 0
    out = capsys.readouterr().out
    assert "METHOD" in out
    assert "PATH" in out
    assert "Total:" in out
    assert "WelcomeEndpoint" in out




