"""Request module exports."""

from pyresponse.request.asgi import Asgi, AsgiRequest
from pyresponse.request.body import Body
from pyresponse.request.envelope import Envelope, RequestEnvelope
from pyresponse.request.fake import Fake
from pyresponse.request.auth_not_found import AuthNotFound, AuthNotFoundError
from pyresponse.request.basic_auth import BasicAuth
from pyresponse.request.bearer_token import BearerToken
from pyresponse.request.cookie import Cookie
from pyresponse.request.cookie_not_found import CookieNotFound, CookieNotFoundError
from pyresponse.request.cookies import Cookies
from pyresponse.request.field_not_found import FieldNotFound, FieldNotFoundError

from pyresponse.request.files import Files
from pyresponse.request.form import Form
from pyresponse.request.head import Head

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
from pyresponse.request.with_params import WithParams


Headers = Head
FormEnvelope = RequestForm

__all__ = [
    # Core Interfaces & Envelopes
    "Request",
    "Envelope",
    "RequestEnvelope",
    "Asgi",
    "AsgiRequest",
    "Fake",
    # Domain Objects & Decorators
    "Head",
    "Headers",
    "Header",
    "Method",
    "Path",
    "PathParam",
    "PathParams",
    "QueryParam",
    "QueryParams",
    "WithParams",
    "Cookie",
    "Cookies",
    "BearerToken",
    "BasicAuth",

    "Json",
    "Multipart",
    "UrlEncoded",
    "RequestForm",
    "FormEnvelope",
    "Form",
    "Files",
    "UploadFile",
    "Body",

    # Domain Exceptions (Fail-Fast)
    "HeaderNotFoundError",
    "HeaderNotFound",
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

]
