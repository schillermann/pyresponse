"""Missing form field domain exception."""

from pyresponse.request.param_not_found import ParamNotFoundError


class FieldNotFoundError(ParamNotFoundError):
    """Raised when a specific form field is requested but not found in the request."""

    def __init__(self, name: str) -> None:
        super().__init__(name)


FieldNotFound = FieldNotFoundError
