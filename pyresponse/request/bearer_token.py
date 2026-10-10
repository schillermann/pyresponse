"""Bearer token authentication extractor."""

from pyresponse.request.auth_not_found import AuthNotFound
from pyresponse.request.authorization import Authorization
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class BearerToken(Envelope):
    """Decorator extracting Bearer authentication token from Authorization header."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._auth = Authorization(origin)

    async def token(self) -> str:
        """Extract and return Bearer token or fail fast with AuthNotFound."""
        raw_auth = (await self._auth.value_or("")).strip()
        if not raw_auth:
            raise AuthNotFound("Bearer")
        parts = raw_auth.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1].strip():
            return parts[1].strip()
        raise AuthNotFound("Bearer")

    async def token_or(self, fallback: str) -> str:
        """Return Bearer token or explicit fallback string."""
        try:
            return await self.token()
        except AuthNotFound:
            return fallback

    async def has(self) -> bool:
        """Check if a valid Bearer token is present in request."""
        try:
            await self.token()
            return True
        except AuthNotFound:
            return False
