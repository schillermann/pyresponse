"""Response decorator invalidating / deleting a cookie."""

from pyresponse.response.cookie import Cookie
from pyresponse.response.envelope import Envelope
from pyresponse.response.response import Response
from pyresponse.response.with_cookie import WithCookie


class WithoutCookie(Envelope):
    """Response decorator invalidating a cookie by setting Max-Age=0 and past expiry."""

    def __init__(
        self,
        origin: Response,
        name: str,
        path: str = "/",
        domain: str = "",
    ) -> None:
        super().__init__(
            WithCookie(
                origin,
                Cookie(
                    name=name,
                    value="",
                    max_age=0,
                    expires="Thu, 01 Jan 1970 00:00:00 GMT",
                    path=path,
                    domain=domain,
                ),
            )
        )

