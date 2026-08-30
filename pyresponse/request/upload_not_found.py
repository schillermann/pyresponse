"""Missing uploaded file domain exception."""

from pyresponse.request.param_not_found import ParamNotFoundError


class UploadNotFoundError(ParamNotFoundError):
    """Raised when an uploaded file is requested but not found in the multipart form."""

    def __init__(self, name: str) -> None:
        super().__init__(name)


UploadNotFound = UploadNotFoundError
