"""Missing upload file domain exception."""

from pyresponse.request.param_not_found import ParamNotFound


class UploadNotFound(ParamNotFound):
    """Raised when an uploaded file is requested but not found."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._name = name

    def name(self) -> str:
        return self._name
