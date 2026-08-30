"""Missing form field domain exception."""

from pyresponse.request.param_not_found import ParamNotFound


class FieldNotFound(ParamNotFound):
    """Raised when a form field is requested but not found."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._name = name

    def name(self) -> str:
        return self._name
