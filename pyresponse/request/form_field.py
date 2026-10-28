"""Multipart form-data text field domain object."""

from pyresponse.request.multipart_part import MultipartPart


class FormField(MultipartPart):
    """Multipart form-data text field part."""

    def __init__(self, name: str, value: str) -> None:
        self._name = name
        self._value = value

    def bytes(self) -> bytes:
        """Encode Content-Disposition header and UTF-8 field value."""
        header = f'Content-Disposition: form-data; name="{self._name}"\r\n\r\n'
        return header.encode("utf-8") + self._value.encode("utf-8")
