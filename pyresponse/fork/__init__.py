"""Fork routing module exports."""

from pyresponse.fork.adapted import Adapted
from pyresponse.fork.callable import Callable
from pyresponse.fork.cors import Cors
from pyresponse.fork.corsed import Corsed
from pyresponse.fork.delete import Delete
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fake import Fake
from pyresponse.fork.fallback import Fallback
from pyresponse.fork.fixed import Fixed
from pyresponse.fork.fork import Fork
from pyresponse.fork.get import Get
from pyresponse.fork.head import Head
from pyresponse.fork.method import Method
from pyresponse.fork.options import Options
from pyresponse.fork.patch import Patch
from pyresponse.fork.path import Path
from pyresponse.fork.post import Post
from pyresponse.fork.prefix import Prefix
from pyresponse.fork.prefixed import Prefixed
from pyresponse.fork.put import Put
from pyresponse.fork.regex import Regex
from pyresponse.fork.route_not_found import RouteNotFound
from pyresponse.fork.sub_path import SubPath
from pyresponse.fork.trap import Trap
from pyresponse.fork.trapped import Trapped
from pyresponse.fork.unmatched import Unmatched
from pyresponse.fork.with_params import WithParams

__all__ = [
    # Core Interfaces
    "Fork",
    "Endpoint",
    "Fallback",
    # Adapters & Decorators
    "Adapted",
    "Callable",
    "Fixed",
    "WithParams",
    "Prefixed",
    "Corsed",
    "Trapped",
    "SubPath",
    "Unmatched",
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
    "Cors",
    "Trap",
    # Domain Exceptions
    "RouteNotFound",
]
