"""CLI process exit code domain object in Pure OOP."""

import sys
from collections.abc import Callable
from typing import Any


class ExitCode(int):
    """Represents a CLI command execution exit code in Pure OOP."""

    def __new__(cls, code: int = 0) -> "ExitCode":
        return super().__new__(cls, code)

    def success(self) -> bool:
        """Check if execution completed successfully."""
        return int(self) == 0

    def failure(self) -> bool:
        """Check if execution failed."""
        return int(self) != 0

    def terminate(self) -> None:
        """Actively terminate the process with this exit code."""
        sys.exit(int(self))

    def apply_to(self, action: Callable[[int], Any]) -> Any:
        """Apply this exit code to a consumer action without exposing internals."""
        return action(int(self))

    def __repr__(self) -> str:
        return f"ExitCode({int(self)})"


class Success(ExitCode):
    """Successful exit code (0)."""

    def __new__(cls) -> "Success":
        return int.__new__(cls, 0)

    def success(self) -> bool:
        return True

    def failure(self) -> bool:
        return False


class Failure(ExitCode):
    """Failure exit code (defaults to 1)."""

    def __new__(cls, code: int = 1) -> "Failure":
        return int.__new__(cls, code)

    def success(self) -> bool:
        return False

    def failure(self) -> bool:
        return True
