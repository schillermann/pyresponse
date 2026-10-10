"""Fork routing module exports in Pure OOP."""

from pyresponse.fork.source_endpoint import SourceEndpoint
from pyresponse.fork.function_endpoint import FunctionEndpoint
from pyresponse.fork.cors import Cors
from pyresponse.fork.cors_endpoint import CorsEndpoint
from pyresponse.fork.delete import Delete
from pyresponse.fork.branch_envelope import BranchEnvelope
from pyresponse.fork.constant_endpoint import ConstantEndpoint
from pyresponse.fork.empty_fork import EmptyFork
from pyresponse.fork.endpoint import Endpoint, Branch, Envelope
from pyresponse.fork.guarded_branch import GuardedBranch
from pyresponse.fork.fake import Fake
from pyresponse.fork.fallback import Fallback
from pyresponse.fork.fork import Fork
from pyresponse.fork.fork_envelope import ForkEnvelope
from pyresponse.fork.logged_fork import LoggedFork
from pyresponse.fork.get import Get
from pyresponse.fork.guarded_endpoint import GuardedEndpoint


from pyresponse.fork.head import Head
from pyresponse.fork.header_fork import HeaderFork
from pyresponse.fork.host import Host
from pyresponse.fork.measured_endpoint import MeasuredEndpoint

from pyresponse.fork.method import Method
from pyresponse.fork.method_branch import MethodBranch
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.fork.options import Options
from pyresponse.fork.patch import Patch
from pyresponse.fork.path import Path
from pyresponse.fork.post import Post
from pyresponse.fork.prefix import Prefix
from pyresponse.fork.prefix_endpoint import PrefixEndpoint
from pyresponse.fork.put import Put
from pyresponse.fork.regex import Regex
from pyresponse.fork.route import Route
from pyresponse.fork.route_entry import EndpointRoutes, FunctionRoutes, RouteEntry
from pyresponse.fork.route_not_found import RouteNotFound
from pyresponse.fork.sub_path import SubPath
from pyresponse.fork.transformed_endpoint import TransformedEndpoint
from pyresponse.fork.trap import Trap
from pyresponse.fork.trap_endpoint import TrapEndpoint
from pyresponse.fork.with_params import WithParams

__all__ = [
    # Core Interfaces
    "Fork",
    "EmptyFork",
    "ForkEnvelope",
    "LoggedFork",
    "Endpoint",
    "Branch",
    "Envelope",

    "BranchEnvelope",
    "Fallback",
    "RouteEntry",
    "EndpointRoutes",
    "FunctionRoutes",
    # Adapters & Decorators
    "SourceEndpoint",
    "FunctionEndpoint",
    "ConstantEndpoint",
    "WithParams",
    "PrefixEndpoint",
    "CorsEndpoint",
    "TrapEndpoint",
    "GuardedEndpoint",
    "GuardedBranch",
    "MeasuredEndpoint",
    "TransformedEndpoint",
    "SubPath",
    "MissingEndpoint",
    "Fake",


    # Routing Forks
    "Path",
    "Route",
    "Regex",
    "Method",
    "MethodBranch",
    "Prefix",
    "Host",
    "HeaderFork",
    "Get",
    "Post",

    "Put",
    "Delete",
    "Patch",
    "Options",
    "Head",
    "Trap",
    "Cors",
    "RouteNotFound",
]
