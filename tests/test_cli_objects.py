"""Tests for Arguments and ExitCode domain objects in pyresponse CLI."""

import pytest

from pyresponse.cli.arguments import ArgumentNotFound, Arguments, ArgumentsFrom, SysArguments
from pyresponse.cli.command import CliCommand, CommandEnvelope, UnknownCommand
from pyresponse.cli.exit_code import ExitCode, Failure, Success
from pyresponse.cli.fork import ForkCli


def test_exit_code_success_and_failure():
    succ = Success()
    assert succ.success() is True
    assert succ.failure() is False
    assert succ == Success()
    assert succ == ExitCode(0)
    assert repr(succ) == "ExitCode(0)"
    assert succ.apply_to(lambda c: c * 10) == 0

    fail = Failure(2)
    assert fail.success() is False
    assert fail.failure() is True
    assert fail == Failure(2)
    assert fail == ExitCode(2)
    assert fail != ExitCode(0)
    assert fail != Success()
    assert repr(fail) == "ExitCode(2)"
    assert fail.apply_to(lambda c: f"code={c}") == "code=2"

    default_fail = Failure()
    assert default_fail == Failure(1)


def test_arguments_operations():
    empty_args = Arguments()
    assert empty_args.empty() is True
    assert bool(empty_args) is False
    assert len(empty_args) == 0
    assert list(empty_args) == []
    assert tuple(empty_args) == ()
    assert empty_args.first_or("fallback") == "fallback"

    with pytest.raises(ArgumentNotFound) as exc_info:
        empty_args.first()
    assert exc_info.value.index() == 0

    with pytest.raises(ArgumentNotFound) as exc_info:
        empty_args.at(0)
    assert exc_info.value.index() == 0

    args = Arguments("serve", "--port", "8080")
    assert args.empty() is False
    assert bool(args) is True
    assert len(args) == 3
    assert tuple(args) == ("serve", "--port", "8080")
    assert args.first() == "serve"
    assert args.at(0) == "serve"
    assert args.at(1) == "--port"
    assert args.at(2) == "8080"
    with pytest.raises(ArgumentNotFound):
        args.at(5)
    assert list(args) == ["serve", "--port", "8080"]

    # Slicing via sub()
    sub_args = args.sub(1)
    assert isinstance(sub_args, Arguments)
    assert tuple(sub_args) == ("--port", "8080")
    assert sub_args == Arguments("--port", "8080")


def test_arguments_from_sequence():
    from_list = ArgumentsFrom(["a", "b", "c"])
    assert tuple(from_list) == ("a", "b", "c")
    assert from_list == Arguments("a", "b", "c")

    from_tuple = ArgumentsFrom(("x", "y"))
    assert tuple(from_tuple) == ("x", "y")
    assert from_tuple == Arguments("x", "y")

    sys_args = SysArguments()
    assert isinstance(sys_args, Arguments)


def test_cli_command_with_arguments_and_exit_code():
    calls: list[Arguments] = []

    class EchoCommand:
        def name(self) -> str:
            return "echo"

        def description(self) -> str:
            return "Echo arguments."

        def matches(self, verb: str) -> bool:
            return verb == "echo"

        def execute(self, args: Arguments) -> ExitCode:
            calls.append(args)
            return Success()

    cmd = EchoCommand()
    assert cmd.name() == "echo"
    assert cmd.matches("echo") is True

    wrapped = CommandEnvelope(cmd)
    res = wrapped.execute(Arguments("hello", "world"))
    assert isinstance(res, ExitCode)
    assert res == Success()
    assert len(calls) == 1
    assert tuple(calls[0]) == ("hello", "world")

    fork = ForkCli([cmd])
    res_fork = fork.execute(Arguments("echo", "foo"))
    assert res_fork == Success()
    assert len(calls) == 2
    assert tuple(calls[1]) == ("foo",)

    # Unknown command returns Failure
    res_unknown = fork.execute(Arguments("unknown_verb"))
    assert isinstance(res_unknown, ExitCode)
    assert res_unknown.failure() is True
    assert res_unknown == Failure(1)
