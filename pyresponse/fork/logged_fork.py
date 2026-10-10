"""Logged fork decorator in Pure OOP."""

from pyresponse.cli.output import ConsoleOutput, Output
from pyresponse.fork.endpoint import Endpoint
from pyresponse.fork.fork import Fork
from pyresponse.fork.fork_envelope import ForkEnvelope
from pyresponse.request.request import Request


class LoggedFork(ForkEnvelope):
    """Fork decorator logging route resolution and matches."""

    def __init__(self, origin: Fork, output: Output = ConsoleOutput()) -> None:
        super().__init__(origin)
        self._output = output

    async def route(self, request: Request) -> Endpoint:
        path = await request.path()
        method = await request.method()
        endpoint = await self._origin.route(request)
        if endpoint.matched():
            self._output.print(f"Matched route: {method} {path}")
        else:
            self._output.print(f"Unmatched route: {method} {path}")
        return endpoint
