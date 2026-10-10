"""pyresponse - A simple web framework in Python that respects pure OOP."""

__version__ = "0.5.0"

from pyresponse import fork, lifespan, request, response
from pyresponse.asgi import AsgiApp
from pyresponse.cli import (
    AliasCommand, Arguments, ArgumentsFrom, CliApp, CliCommand, CliRoutes,
    DiscoveredCommands, ExitCode, Failure, FixedRoutes, ForkCli, HelpCommand,
    RouteEntry, Routes, RoutesCommand, RoutesTable, ServeCommand, SourceRoutes,
    Success, SysArguments, TableRow, UnknownCommand,
)
from pyresponse.error import Error
from pyresponse.fork import (
    ConstantEndpoint, CorsEndpoint, Delete, Endpoint, EndpointRoutes, Fallback,
    Fork, FunctionEndpoint, FunctionRoutes, Get, Method, MissingEndpoint,
    Options, Patch, Post, Prefix, PrefixEndpoint, Put, Regex, Route,
    RouteNotFound, SourceEndpoint, Trap, TrapEndpoint,
)
from pyresponse.lifespan import (
    Fake as Fake, ForkLifespan, Lifespan, WithShutdown, WithStartup,
)
from pyresponse.request import (
    Asgi, AuthNotFound, Authorization, BasicAuth, BearerToken, Cookie,
    CookieNotFound, Cookies, Envelope as Envelope, FieldNotFound, Files, Form,
    Head as RequestHead, Header, HeaderNotFound, Multipart, ParamNotFound,
    Path as RequestPath, PathParam, PathParams, QueryParam, QueryParams,
    Request, RequestForm, Sticky, UploadFile, UploadNotFound, UrlEncoded,
    WithHeader, WithMethod, WithPath, WithQuery,
)
from pyresponse.response import (
    BadRequest, Binary, Body, BytesBody, Created, Json, NoCache, NoContent,
    NotFound, Ok, Redirect, Response, ServerError, Sse, StatusLine, StreamBody,
    Text, TextBody, WithBody, WithCookie, WithoutCookie,
)
from pyresponse.server import Server

__all__ = [
    "__version__",
    # Submodules
    "fork", "request", "response", "lifespan",
    # Core Interfaces & App
    "AsgiApp", "Server", "Error", "Request", "Response", "Endpoint", "Fork",
    "Fallback", "Lifespan", "WithStartup", "WithShutdown", "ForkLifespan",
    "Fake", "SourceEndpoint", "FunctionEndpoint", "ConstantEndpoint",
    "CorsEndpoint", "PrefixEndpoint", "TrapEndpoint", "MissingEndpoint",
    # Forks & Routing
    "Delete", "Get", "Method", "Options", "Patch", "Post", "Prefix", "Put",
    "Regex", "Route", "Trap", "RouteNotFound", "EndpointRoutes", "FunctionRoutes",
    # Request Objects
    "Envelope", "Header", "RequestHead", "RequestPath", "Asgi", "Cookies",
    "Cookie", "QueryParams", "QueryParam", "PathParams", "PathParam",
    "WithHeader", "WithQuery", "WithMethod", "WithPath", "Form", "Files",
    "UploadFile", "Multipart", "UrlEncoded", "Authorization", "BearerToken",
    "BasicAuth", "Sticky", "RequestForm",
    # Response Objects
    "StatusLine", "Ok", "NotFound", "BadRequest", "ServerError", "Created",
    "NoContent", "Json", "Text", "Binary", "Sse", "Redirect", "WithCookie",
    "WithoutCookie", "Body", "BytesBody", "StreamBody", "TextBody", "WithBody",
    "NoCache",
    # Errors
    "HeaderNotFound", "ParamNotFound", "CookieNotFound", "AuthNotFound",
    "FieldNotFound", "UploadNotFound",
    # CLI
    "CliApp", "ForkCli", "CliCommand", "AliasCommand", "UnknownCommand",
    "HelpCommand", "ServeCommand", "RoutesCommand", "SourceRoutes",
    "RoutesTable", "TableRow", "RouteEntry", "Routes", "CliRoutes",
    "FixedRoutes", "DiscoveredCommands", "Arguments", "ArgumentsFrom",
    "SysArguments", "ExitCode", "Success", "Failure",
]
