"""Protocol representing an individual RFC 7578 multipart/form-data part."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class MultipartPart(Protocol):
    """Abstract multipart/form-data section producing its own header and payload bytes."""

    def bytes(self) -> bytes:
        """Return encoded part headers and body payload without boundary markers."""
        ...
