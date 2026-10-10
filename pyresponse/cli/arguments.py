"""CLI arguments domain object in Pure OOP."""

import sys
from collections.abc import Iterator, Sequence

from pyresponse.error import Error


class ArgumentNotFound(Error):
    """Raised when an expected CLI argument is missing."""

    def __init__(self, index: int) -> None:
        super().__init__(f"CLI argument at index {index} is missing.")
        self._index = index

    def index(self) -> int:
        return self._index


class Arguments:
    """CLI arguments encapsulated in Pure OOP."""

    def __init__(self, *args: str) -> None:
        self._args = args

    def empty(self) -> bool:
        """Check if arguments are empty."""
        return len(self._args) == 0

    def first(self) -> str:
        """Return the first argument, failing fast if missing."""
        return self.at(0)

    def first_or(self, fallback: str) -> str:
        """Return the first argument or the given fallback."""
        return self.at_or(0, fallback)

    def at(self, index: int) -> str:
        """Return the argument at the given index, failing fast if missing."""
        if 0 <= index < len(self._args):
            return self._args[index]
        raise ArgumentNotFound(index)

    def at_or(self, index: int, fallback: str) -> str:
        """Return the argument at the given index or the given fallback."""
        if 0 <= index < len(self._args):
            return self._args[index]
        return fallback

    def sub(self, start: int = 1) -> "Arguments":
        """Return a slice of arguments starting from index."""
        return Arguments(*self._args[start:])

    def __bool__(self) -> bool:
        return not self.empty()

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self) -> Iterator[str]:
        return iter(self._args)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Arguments):
            return self._args == other._args
        return False

    def __repr__(self) -> str:
        return f"Arguments{self._args}"


class ArgumentsFrom(Arguments):
    """Secondary constructor instantiating Arguments from a Sequence."""

    def __init__(self, items: Sequence[str]) -> None:
        super().__init__(*items)


class SysArguments(Arguments):
    """Secondary constructor instantiating Arguments directly from sys.argv."""

    def __init__(self) -> None:
        super().__init__(*sys.argv[1:])
