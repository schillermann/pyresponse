"""Quick Start entry point for pyresponse."""

from pyresponse import Server
from pyresponse.response import Ok, Body, Header

app = Server(
    lambda request: (
        Ok(
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
