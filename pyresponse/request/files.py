"""Parsed multipart files representation."""

from types import MappingProxyType
from typing import Mapping, Sequence

from pyresponse.request.upload_file import UploadFile
from pyresponse.request.upload_not_found import UploadNotFound


class Files:
    """Parsed multipart uploaded files domain representation."""

    def __init__(
        self,
        files: Mapping[str, Sequence[UploadFile]] = MappingProxyType({}),
    ) -> None:
        self._files = files

    def file(self, name: str) -> UploadFile:
        """Return uploaded file or fail fast with UploadNotFound."""
        if name in self._files and self._files[name]:
            return self._files[name][0]
        raise UploadNotFound(name)

    def file_or(self, name: str, fallback: UploadFile) -> UploadFile:
        """Return uploaded file or explicit fallback file."""
        if name in self._files and self._files[name]:
            return self._files[name][0]
        return fallback

    def file_list(self, name: str) -> Sequence[UploadFile]:
        """Return all files associated with a field name."""
        return self._files.get(name, ())

    def has(self, name: str) -> bool:
        """Check if uploaded file is present."""
        return name in self._files
