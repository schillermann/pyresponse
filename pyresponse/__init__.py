"""pyresponse - A simple web framework in Python that respects pure OOP."""

from pyresponse import fork, request, response
from pyresponse.asgi import AsgiApp
from pyresponse.errors import (
    HeaderNotFoundError,
    ParamNotFoundError,
    PyResponseError,
    RouteNotFoundError,
)
from pyresponse.fork import Endpoint, Fork, Page
from pyresponse.protocol import FakeLifespan, Lifespan
from pyresponse.response.no_content import NoContent
from pyresponse.response.statusline import (
    OK,
    BadRequest,
    Created,
    NotFound,
    Ok,
    ServerError,
    StatusLine,
)
from pyresponse.server import Server

__all__ = [
    # Submodules
    "fork",
    "request",
    "response",
    # Protocols & Core Domain
    "Endpoint",
    "Page",
    "Fork",
    "Lifespan",
    "FakeLifespan",
    # Status Lines & Responses
    "OK",
    "Ok",
    "Created",
    "NoContent",
    "BadRequest",
    "NotFound",
    "ServerError",
    "StatusLine",
    # Domain Errors (Fail-Fast)
    "PyResponseError",
    "HeaderNotFoundError",
    "RouteNotFoundError",
    "ParamNotFoundError",
    # Server & ASGI
    "Server",
    "AsgiApp",
]
