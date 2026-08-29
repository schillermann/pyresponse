"""Quick Start example for pyresponse framework."""

from pyresponse import Server
from pyresponse.response import OK, Body, Header

app = Server(
    lambda request: (
        OK(
            Header(
                Body("<h1>Hello from PyResponse!</h1>"),
                "Content-Type",
                "text/html",
            )
        )
    ),
    port=8000,
)

if __name__ == "__main__":
    app.start()
