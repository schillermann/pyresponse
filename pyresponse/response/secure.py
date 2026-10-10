"""Composite Secure response decorator in Pure OOP."""

from pyresponse.response.envelope import Envelope
from pyresponse.response.frame_options import FrameOptions
from pyresponse.response.hsts import Hsts
from pyresponse.response.no_sniff import NoSniff
from pyresponse.response.response import Response


class Secure(Envelope):
    """Response decorator composing HSTS, NoSniff, and FrameOptions security headers."""

    def __init__(
        self,
        origin: Response,
        frame_option: str = "DENY",
        hsts_max_age: int = 31536000,
        include_subdomains: bool = True,
    ) -> None:
        super().__init__(
            Hsts(
                NoSniff(FrameOptions(origin, frame_option)),
                max_age=hsts_max_age,
                include_subdomains=include_subdomains,
            )
        )
