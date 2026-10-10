"""Guarded branch decorator in Pure OOP."""

import inspect
from collections.abc import Callable as TypingCallable
from typing import Any

from pyresponse.fork.branch_envelope import BranchEnvelope
from pyresponse.fork.endpoint import Branch, Endpoint
from pyresponse.fork.missing_endpoint import MissingEndpoint
from pyresponse.request.request import Request


class GuardedBranch(BranchEnvelope):
    """Branch decorator evaluating routes only when guard condition passes."""

    def __init__(
        self,
        origin: Branch,
        guard: TypingCallable[[Request], Any],
    ) -> None:
        super().__init__(origin)
        self._guard = guard

    async def route(self, request: Request) -> Endpoint:
        passed = self._guard(request)
        if inspect.isawaitable(passed):
            passed = await passed
        if not passed:
            return MissingEndpoint()
        return await self._origin.route(request)
