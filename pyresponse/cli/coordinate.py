"""Target coordinates for module and attribute in Pure OOP."""

from typing import Protocol

__all__ = [
    "Coordinate",
    "ExplicitCoordinate",
    "TextCoordinate",
]


class Coordinate(Protocol):
    """Protocol representing a module and attribute target coordinate."""

    def module_name(self) -> str:
        ...

    def attribute_name(self) -> str:
        ...


class ExplicitCoordinate:
    """Target coordinate explicitly provided as module and attribute names."""

    def __init__(self, module: str, attribute: str = "app") -> None:
        self._module = module
        self._attribute = attribute

    def module_name(self) -> str:
        return self._module

    def attribute_name(self) -> str:
        return self._attribute

    def __str__(self) -> str:
        return f"{self._module}:{self._attribute}"


class TextCoordinate:
    """Target coordinate parsed from a raw 'module:attribute' or 'module' text string."""

    def __init__(self, raw: str, default_attr: str = "app") -> None:
        self._raw = raw
        self._default_attr = default_attr

    def module_name(self) -> str:
        if ":" in self._raw:
            return self._raw.split(":", 1)[0]
        return self._raw

    def attribute_name(self) -> str:
        if ":" in self._raw:
            return self._raw.split(":", 1)[1]
        return self._default_attr

    def __str__(self) -> str:
        return f"{self.module_name()}:{self.attribute_name()}"
