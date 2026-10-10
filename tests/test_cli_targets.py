"""Tests for CLI target resolution and coordinates."""

import os
import sys

from pyresponse.cli.candidate import FileCandidate
from pyresponse.cli.coordinate import ExplicitCoordinate, TextCoordinate
from pyresponse.cli.directory import CurrentDirectory, CustomDirectory
from pyresponse.cli.in_path_target import InPathTarget
from pyresponse.cli.output import MemoryOutput
from pyresponse.cli.routes import RouteEntry, TableRow
from pyresponse.cli.target import ArgumentTarget, ExplicitTarget


def test_target_coordinate() -> None:
    c1 = TextCoordinate("api.v1:my_app")
    assert c1.module_name() == "api.v1"
    assert c1.attribute_name() == "my_app"
    assert str(c1) == "api.v1:my_app"

    c2 = TextCoordinate("server")
    assert c2.module_name() == "server"
    assert c2.attribute_name() == "app"

    c3 = ExplicitCoordinate("backend", "server")
    assert c3.module_name() == "backend"
    assert c3.attribute_name() == "server"
    assert str(c3) == "backend:server"


def test_file_candidate() -> None:
    cand = FileCandidate("main.py", "app")
    assert cand.exists() is True
    assert cand.target().name() == "main:app"

    missing = FileCandidate("does_not_exist_xyz.py")
    assert missing.exists() is False


def test_directory_objects() -> None:
    curr = CurrentDirectory()
    assert os.path.isdir(curr.path())

    custom = CustomDirectory("/custom/dir")
    assert custom.path() == "/custom/dir"

    cand = FileCandidate("main.py", "app", curr)
    assert cand.exists() is True


def test_in_path_target() -> None:
    cwd = os.getcwd()
    target = InPathTarget([cwd], ExplicitTarget(TextCoordinate("main:app")))
    assert target.name() == "main:app"
    _ = target.load()
    assert cwd in sys.path


def test_specified_target() -> None:
    fallback = ExplicitTarget(TextCoordinate("main:app"))
    specified = ArgumentTarget("quick_start:app", fallback)
    assert specified.name() == "quick_start:app"

    unspecified = ArgumentTarget("", fallback)
    assert unspecified.name() == "main:app"


def test_table_row() -> None:
    entry = RouteEntry("GET", "/api/items", "ItemEndpoint")
    row = TableRow(entry, 6, 12).text()
    assert "GET" in row
    assert "/api/items" in row
    assert "ItemEndpoint" in row


def test_memory_output() -> None:
    out = MemoryOutput()
    out.print("hello")
    out.error("oops")
    assert out.stdout() == "hello"
    assert out.stderr() == "oops"


def test_routable_endpoint() -> None:
    from pyresponse.fork.route_entry import EndpointRoutes, FunctionRoutes
    from pyresponse.request import Request
    from pyresponse.response import Response, Text

    def my_fn(req: Request) -> Response:
        return Text("hi")

    entries = EndpointRoutes(my_fn).routes("/prefix")
    assert len(entries) == 1
    assert entries[0].method() == "ANY"
    assert entries[0].path() == "/prefix"
    assert entries[0].handler() == "my_fn"

    fn_entries = FunctionRoutes(my_fn).routes("/sub")
    assert len(fn_entries) == 1
    assert fn_entries[0].path() == "/sub"


def test_routes_objects() -> None:
    from pyresponse.cli.routes import CliRoutes, FixedRoutes, SourceRoutes
    from pyresponse.fork import Fork, Path
    from pyresponse.response import Body, Ok

    cli_routes = CliRoutes("main:app")
    assert len(cli_routes.entries()) == 1

    fork = Fork(Path("/test", lambda req: Ok(Body("ok"))))
    fixed_routes = FixedRoutes(fork)
    entries = fixed_routes.entries()
    assert len(entries) == 1
    assert entries[0].path() == "/test"

    source_routes = SourceRoutes(fork)
    assert len(source_routes.entries()) == 1

