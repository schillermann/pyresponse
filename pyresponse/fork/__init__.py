"""Fork routing module exports."""

from pyresponse.fork.as_endpoint import AsEndpoint
from pyresponse.fork.callable import Callable, CallableEndpoint
from pyresponse.fork.delete import Delete
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fake import Fake
from pyresponse.fork.fallback import Fallback
from pyresponse.fork.fork import Fork
from pyresponse.fork.get import Get
from pyresponse.fork.head import Head
from pyresponse.fork.method import Method
from pyresponse.fork.options import Options
from pyresponse.fork.patch import Patch
from pyresponse.fork.path import Path
from pyresponse.fork.post import Post
from pyresponse.fork.prefix import Prefix
from pyresponse.fork.prefixed import Prefixed, PrefixedEndpoint
from pyresponse.fork.put import Put
from pyresponse.fork.regex import Regex
from pyresponse.fork.route_not_found import RouteNotFound, RouteNotFoundError
from pyresponse.fork.sub_path import SubPath
from pyresponse.fork.trap import Catch, Trap
from pyresponse.fork.trapped import Trapped, TrappedEndpoint
from pyresponse.fork.unmatched import Unmatched, UnmatchedEndpoint
from pyresponse.fork.with_params import EndpointWithParams, WithParams

Page = Path

__all__ = [
    # Core Interfaces
    "Fork",
    "Endpoint",
    "Fallback",
    "Page",
    # Adapters & Decorators
    "AsEndpoint",
    "Callable",
    "CallableEndpoint",
    "WithParams",
    "EndpointWithParams",
    "Prefixed",
    "PrefixedEndpoint",
    "Trapped",
    "TrappedEndpoint",
    "SubPath",
    "Unmatched",
    "UnmatchedEndpoint",
    "Fake",
    # Routing Forks
    "Path",
    "Regex",
    "Method",
    "Prefix",
    "Get",
    "Post",
    "Put",
    "Delete",
    "Patch",
    "Options",
    "Head",
    "Trap",
    "Catch",
    # Domain Exceptions
    "RouteNotFoundError",
    "RouteNotFound",
]
