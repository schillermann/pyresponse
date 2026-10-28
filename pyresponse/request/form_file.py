"""Multipart form-data binary file domain object."""

from pyresponse.request.multipart_part import MultipartPart


class FormFile(MultipartPart):
    """Multipart form-data binary file part."""

    def __init__(
        self,
        name: str,
        filename: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        self._name = name
        self._filename = filename
        self._content = content
        self._content_type = content_type

    def bytes(self) -> bytes:
        """Encode Content-Disposition, Content-Type headers, and raw binary content."""
        header = (
            f'Content-Disposition: form-data; name="{self._name}"; '
            f'filename="{self._filename}"\r\n'
            f"Content-Type: {self._content_type}\r\n\r\n"
        )
        return header.encode("utf-8") + self._content
