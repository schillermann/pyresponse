"""Domain exception raised when an ASGI application fails to start an HTTP response."""

from pyresponse.error import Error


class AsgiNotStarted(Error):
    """Raised when an ASGI 3.0 application completes without sending http.response.start."""

    pass
