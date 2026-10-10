"""CLI entry point for pyresponse in Pure OOP."""

from pyresponse.cli.app import CliApp
from pyresponse.cli.arguments import Arguments, SysArguments
from pyresponse.cli.exit_code import ExitCode


def main(args: Arguments = SysArguments()) -> ExitCode:
    return CliApp().execute(args)


if __name__ == "__main__":
    main().terminate()
