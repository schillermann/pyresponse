"""CLI entry point for pyresponse."""

import sys
from pyresponse.cli.app import CliApp


def main(args: list[str] | None = None) -> int:
    cmd_args = sys.argv[1:] if args is None else args
    return CliApp().execute(cmd_args)


if __name__ == "__main__":
    sys.exit(main())
