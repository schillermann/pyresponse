"""Application target loader for pyresponse CLI in Pure OOP."""

import importlib
import os
import sys
from typing import Any, Protocol, Sequence

from pyresponse.cli.candidate import Candidate, FileCandidate
from pyresponse.cli.coordinate import Coordinate, ExplicitCoordinate, TextCoordinate
from pyresponse.cli.directory import CurrentDirectory, CustomDirectory, Directory
from pyresponse.error import Error
from pyresponse.fork.route_entry import EndpointRoutes, RouteEntry

__all__ = [
    "TargetNotFound",
    "Target",
    "Coordinate",
    "ExplicitCoordinate",
    "TextCoordinate",
    "Directory",
    "CurrentDirectory",
    "CustomDirectory",
    "Candidate",
    "ExplicitTarget",
    "InPathTarget",
    "FileCandidate",
    "TargetEnvelope",
    "ArgumentTarget",
    "EnvTarget",
    "CandidateTarget",
    "AppTarget",
]


from pyresponse.cli.explicit_target import ExplicitTarget, TargetNotFound


class Target(Protocol):
    """Protocol for an application target."""

    def name(self) -> str:
        ...

    def load(self) -> Any:
        ...

    def routes(self) -> Sequence[RouteEntry]:
        ...


from pyresponse.cli.in_path_target import InPathTarget
from pyresponse.cli.target_envelope import TargetEnvelope


class ArgumentTarget:
    """Target specified as a non-empty string argument, falling back to another target."""

    def __init__(self, value: str, fallback: Target) -> None:
        self._value = value
        self._fallback = fallback

    def target(self) -> Target:
        if self._value:
            return ExplicitTarget(TextCoordinate(self._value))
        return self._fallback

    def name(self) -> str:
        return self.target().name()

    def load(self) -> Any:
        return self.target().load()

    def routes(self) -> Sequence[RouteEntry]:
        return self.target().routes()


class EnvTarget:
    """Target loaded from an environment variable if set, otherwise falls back."""

    def __init__(self, key: str, fallback: Target) -> None:
        self._key = key
        self._fallback = fallback

    def target(self) -> Target:
        val = os.getenv(self._key, "")
        if val:
            return ExplicitTarget(TextCoordinate(val))
        return self._fallback

    def name(self) -> str:
        return self.target().name()

    def load(self) -> Any:
        return self.target().load()

    def routes(self) -> Sequence[RouteEntry]:
        return self.target().routes()


class CandidateTarget:
    """Selects target among candidate domain objects."""

    def __init__(
        self,
        candidates: Sequence[Candidate],
        fallback: Target,
    ) -> None:
        self._candidates = candidates
        self._fallback = fallback

    def target(self) -> Target:
        for candidate in self._candidates:
            if candidate.exists():
                return candidate.target()
        return self._fallback

    def name(self) -> str:
        return self.target().name()

    def load(self) -> Any:
        return self.target().load()

    def routes(self) -> Sequence[RouteEntry]:
        return self.target().routes()


class AppTarget(Target):
    """Composite entrypoint for target loading in Pure OOP."""

    def __init__(self, target: str = "") -> None:
        self._target = target

    def target(self) -> Target:
        cwd = CurrentDirectory().path()
        parent = os.path.dirname(cwd)
        return InPathTarget(
            (
                cwd,
                os.path.join(cwd, "backend"),
                parent,
                os.path.join(parent, "backend"),
            ),
            ArgumentTarget(
                self._target,
                EnvTarget(
                    "PYRESPONSE_APP",
                    CandidateTarget(
                        (
                            FileCandidate("main.py", "app"),
                            FileCandidate("app.py", "app"),
                            FileCandidate("server.py", "app"),
                        ),
                        ExplicitTarget(TextCoordinate("main:app")),
                    ),
                ),
            ),
        )

    def name(self) -> str:
        return self.target().name()

    def load(self) -> Any:
        return self.target().load()

    def routes(self) -> Sequence[RouteEntry]:
        return self.target().routes()
