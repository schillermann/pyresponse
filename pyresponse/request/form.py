"""Parsed form fields representation."""

from types import MappingProxyType
from typing import Mapping, Sequence

from pyresponse.request.field_not_found import FieldNotFound


class Form:
    """Parsed form text fields domain representation."""

    def __init__(
        self,
        fields: Mapping[str, Sequence[str]] = MappingProxyType({}),
    ) -> None:
        self._fields = fields

    def field(self, name: str) -> str:
        """Return field value or fail fast with FieldNotFound."""
        if name in self._fields and self._fields[name]:
            return self._fields[name][0]
        raise FieldNotFound(name)

    def field_or(self, name: str, fallback: str) -> str:
        """Return field value or explicit fallback string."""
        if name in self._fields and self._fields[name]:
            return self._fields[name][0]
        return fallback

    def field_list(self, name: str) -> Sequence[str]:
        """Return all values associated with a field name."""
        return self._fields.get(name, ())

    def has(self, name: str) -> bool:
        """Check if form field is present."""
        return name in self._fields



