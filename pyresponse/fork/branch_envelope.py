"""Branch envelope decorator in Pure OOP."""

from pyresponse.fork.endpoint import Branch, Endpoint
from pyresponse.request.request import Request


class BranchEnvelope(Branch):
    """Base class for router branch decorators implementing the envelope pattern."""

    def __init__(self, origin: Branch) -> None:
        self._origin = origin

    async def route(self, request: Request) -> Endpoint:
        return await self._origin.route(request)
