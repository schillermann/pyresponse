"""Uploaded multipart file encapsulation."""

from pyresponse.request.head import Head


class UploadFile:
    """Encapsulation of an uploaded multipart file."""

    def __init__(
        self,
        filename: str,
        content_type: str,
        content: bytes,
        head: Head = Head(),
    ) -> None:
        self._filename = filename
        self._content_type = content_type
        self._content = content
        self._head = head

    def filename(self) -> str:
        return self._filename

    def content_type(self) -> str:
        return self._content_type

    def head(self) -> Head:
        """Return the MIME head metadata for this uploaded part."""
        return self._head

    async def read(self) -> bytes:
        return self._content

    def size(self) -> int:
        return len(self._content)
