"""CLI process exit code domain object in Pure OOP."""

import sys
from collections.abc import Callable
from typing import Any


class ExitCode:
    """Represents a CLI command execution exit code in Pure OOP."""

    def __init__(self, code: int = 0) -> None:
        self._code = code

    def success(self) -> bool:
        """Check if execution completed successfully."""
        return self._code == 0

    def failure(self) -> bool:
        """Check if execution failed."""
        return self._code != 0

    def terminate(self) -> None:
        """Actively terminate the process with this exit code."""
        sys.exit(self._code)

    def apply_to(self, action: Callable[[int], Any]) -> Any:
        """Apply this exit code to a consumer action without exposing internals."""
        return action(self._code)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExitCode):
            return self._code == other._code
        return False

    def __repr__(self) -> str:
        return f"ExitCode({self._code})"


class Success(ExitCode):
    """Successful exit code (0)."""

    def __init__(self) -> None:
        super().__init__(0)

    def success(self) -> bool:
        return True

    def failure(self) -> bool:
        return False


class Failure(ExitCode):
    """Failure exit code (defaults to 1)."""

    def __init__(self, code: int = 1) -> None:
        super().__init__(code)

    def success(self) -> bool:
        return False

    def failure(self) -> bool:
        return True
