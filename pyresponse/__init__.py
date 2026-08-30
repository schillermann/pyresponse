"""pyresponse - A simple web framework in Python that respects pure OOP."""

__version__ = "0.1.0"

from pyresponse import fork, lifespan, request, response
from pyresponse.asgi import AsgiApp
from pyresponse.error import Error, PyResponseError
from pyresponse.fork import (
    Adapted,
    Catch,
    Delete,
    Endpoint,
    Fallback,
    Fixed,
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
    Regex,
    RouteNotFound,
    RouteNotFoundError,
    Trap,
)
from pyresponse.fork.cors import Cors as CorsFork
from pyresponse.fork.corsed import Corsed


from pyresponse.lifespan import FakeLifespan, Lifespan
from pyresponse.request.asgi import Asgi, AsgiRequest
from pyresponse.request.auth_not_found import AuthNotFound, AuthNotFoundError
from pyresponse.request.basic_auth import BasicAuth
from pyresponse.request.bearer_token import BearerToken
from pyresponse.request.cookie import Cookie
from pyresponse.request.cookie_not_found import CookieNotFound, CookieNotFoundError
from pyresponse.request.cookies import Cookies
from pyresponse.request.envelope import Envelope as RequestEnvelope
from pyresponse.request.field_not_found import FieldNotFound, FieldNotFoundError
from pyresponse.request.files import Files
from pyresponse.request.form import Form
from pyresponse.request.header import Header
from pyresponse.request.header_not_found import HeaderNotFound, HeaderNotFoundError
from pyresponse.request.json import Json
from pyresponse.request.method import Method
from pyresponse.request.multipart import Multipart
from pyresponse.request.param_not_found import ParamNotFound, ParamNotFoundError
from pyresponse.request.path import Path
from pyresponse.request.path_param import PathParam
from pyresponse.request.path_params import PathParams
from pyresponse.request.query_param import QueryParam
from pyresponse.request.query_params import QueryParams
from pyresponse.request.request import Request
from pyresponse.request.request_form import RequestForm
from pyresponse.request.upload_file import UploadFile
from pyresponse.request.upload_not_found import UploadNotFound, UploadNotFoundError
from pyresponse.request.urlencoded import UrlEncoded

from pyresponse.response.binary import Binary
from pyresponse.response.body import Body
from pyresponse.response.cookie import Cookie as ResponseCookie
from pyresponse.response.cors import Cors
from pyresponse.response.envelope import Envelope as ResponseEnvelope
from pyresponse.response.no_content import NoContent
from pyresponse.response.redirect import Redirect
from pyresponse.response.response import Response
from pyresponse.response.sse import Sse
from pyresponse.response.text import Text
from pyresponse.response.with_body import WithBody
from pyresponse.response.with_cookie import WithCookie
from pyresponse.response.without_cookie import WithoutCookie



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
    "Adapted",
    "Asgi",

    "AsgiRequest",
    "RequestEnvelope",
    "ResponseEnvelope",
    "Form",
    "Files",
    "RequestForm",
    "UrlEncoded",
    "Multipart",
    "UploadFile",
    "QueryParam",
    "QueryParams",
    "PathParam",
    "PathParams",
    "Header",
    "Json",
    "Cookie",
    "Cookies",
    "BearerToken",
    "BasicAuth",

    # Routing Forks
    "Prefix",
    "Method",
    "Get",
    "Post",
    "Put",
    "Delete",
    "Patch",
    "Options",
    "Regex",
    "ForkHead",
    "CorsFork",
    "Corsed",
    "Fixed",
    "Trap",
    "Catch",



    # Status Lines & Responses
    "Body",
    "WithBody",
    "Text",
    "Binary",
    "Sse",
    "Redirect",
    "OK",
    "Ok",
    "Created",
    "NoContent",
    "BadRequest",
    "NotFound",
    "ServerError",
    "StatusLine",
    "Cors",
    "WithCookie",
    "WithoutCookie",




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
    "CookieNotFoundError",
    "CookieNotFound",
    "AuthNotFoundError",
    "AuthNotFound",

    # Server & ASGI
    "Server",
    "AsgiApp",
]
