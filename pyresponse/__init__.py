"""pyresponse - A simple web framework in Python that respects pure OOP."""

__version__ = "0.1.0"

from pyresponse import fork, lifespan, request, response
from pyresponse.asgi import AsgiApp
from pyresponse.error import Error, PyResponseError
from pyresponse.fork import (
    AsEndpoint,
    Catch,
    Delete,
    Endpoint,
    Fallback,
    Fork,
    Get,
    Head as ForkHead,
    Method,
    Options,
    Page,
    Patch,
    Post,
    Prefix,
    Put,
    RouteNotFound,
    RouteNotFoundError,
    Trap,
)
from pyresponse.lifespan import FakeLifespan, Lifespan
from pyresponse.request.asgi import Asgi, AsgiRequest
from pyresponse.request.envelope import Envelope as RequestEnvelope
from pyresponse.request.field_not_found import FieldNotFound, FieldNotFoundError
from pyresponse.request.form import Form
from pyresponse.request.header_not_found import HeaderNotFound, HeaderNotFoundError
from pyresponse.request.param_not_found import ParamNotFound, ParamNotFoundError
from pyresponse.request.request import Request
from pyresponse.request.upload_file import UploadFile
from pyresponse.request.upload_not_found import UploadNotFound, UploadNotFoundError
from pyresponse.response.envelope import Envelope as ResponseEnvelope
from pyresponse.response.no_content import NoContent
from pyresponse.response.response import Response
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
    "__version__",
    # Submodules
    "fork",
    "request",
    "response",
    "lifespan",
    # Protocols & Core Domain
    "Request",
    "Response",
    "Endpoint",
    "Page",
    "Fork",
    "Fallback",
    "Lifespan",
    "FakeLifespan",
    "AsEndpoint",
    "Asgi",
    "AsgiRequest",
    "RequestEnvelope",
    "ResponseEnvelope",
    "Form",
    "UploadFile",
    # Routing Forks
    "Prefix",
    "Method",
    "Get",
    "Post",
    "Put",
    "Delete",
    "Patch",
    "Options",
    "ForkHead",
    "Trap",
    "Catch",
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
    "Error",
    "PyResponseError",
    "HeaderNotFoundError",
    "HeaderNotFound",
    "RouteNotFoundError",
    "RouteNotFound",
    "ParamNotFoundError",
    "ParamNotFound",
    "FieldNotFoundError",
    "FieldNotFound",
    "UploadNotFoundError",
    "UploadNotFound",
    # Server & ASGI
    "Server",
    "AsgiApp",
]
