"""Parsed multipart / form representation."""

from types import MappingProxyType
from typing import Mapping, Sequence

from pyresponse.request.field_not_found import FieldNotFoundError
from pyresponse.request.upload_file import UploadFile
from pyresponse.request.upload_not_found import UploadNotFoundError


class Form:
    """Parsed multipart / form representation."""

    def __init__(
        self,
        fields: Mapping[str, Sequence[str]] = MappingProxyType({}),
        files: Mapping[str, Sequence[UploadFile]] = MappingProxyType({}),
    ) -> None:
        self._fields = fields
        self._files = files

    def field(self, name: str, default: str = "") -> str:
        """Return field value, returning default if provided or failing fast with FieldNotFoundError."""
        if name in self._fields and self._fields[name]:
            return self._fields[name][0]
        if default:
            return default
        raise FieldNotFoundError(name)

    def field_or(self, name: str, fallback: str) -> str:
        """Return field value or explicit fallback string."""
        if name in self._fields and self._fields[name]:
            return self._fields[name][0]
        return fallback

    def field_list(self, name: str) -> Sequence[str]:
        """Return all values associated with a field name."""
        return self._fields.get(name, ())

    def file(self, name: str, default: UploadFile | None = None) -> UploadFile:
        """Return uploaded file, returning default if provided or failing fast with UploadNotFoundError."""
        if name in self._files and self._files[name]:
            return self._files[name][0]
        if default is not None:
            return default
        raise UploadNotFoundError(name)

    def file_or(self, name: str, fallback: UploadFile) -> UploadFile:
        """Return uploaded file or explicit fallback file."""
        if name in self._files and self._files[name]:
            return self._files[name][0]
        return fallback

    def file_list(self, name: str) -> Sequence[UploadFile]:
        """Return all files associated with a field name."""
        return self._files.get(name, ())

    def has(self, name: str) -> bool:
        """Check if form field is present."""
        return name in self._fields

    def has_file(self, name: str) -> bool:
        """Check if uploaded file is present."""
        return name in self._files
