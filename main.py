"""Main entry point for pyresponse."""

from pyresponse import Server
from pyresponse.fork.endpoint import Endpoint
from pyresponse.request.request import Request
from pyresponse.response import Body, Header, Ok, Response


class WelcomeEndpoint(Endpoint):
    """Greeting endpoint rendering HTML response."""

    def matched(self) -> bool:
        return True

    async def response(self, request: Request) -> Response:
        return Ok(
            Header(
                Body("<h1>Hello from PyResponse!</h1>"),
                "Content-Type",
                "text/html",
            )
        )


class MainApp:
    """Application root creating the server instance."""

    def server(self) -> Server:
        return Server(WelcomeEndpoint(), port=8000)


app = MainApp().server()

if __name__ == "__main__":
    app.start()
