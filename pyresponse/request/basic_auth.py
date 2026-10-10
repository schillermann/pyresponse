"""HTTP Basic authentication extractor."""

import base64
from pyresponse.request.auth_not_found import AuthNotFound
from pyresponse.request.authorization import Authorization
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class BasicAuth(Envelope):
    """Decorator extracting Basic authentication username and password from Authorization header."""

    def __init__(self, origin: Request) -> None:
        super().__init__(origin)
        self._auth = Authorization(origin)

    async def credentials(self) -> tuple[str, str]:
        """Extract and return (username, password) tuple or fail fast with AuthNotFound."""
        raw_auth = (await self._auth.value_or("")).strip()
        if not raw_auth:
            raise AuthNotFound("Basic")
        parts = raw_auth.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "basic":
            raise AuthNotFound("Basic")
        try:
            decoded = base64.b64decode(parts[1].strip()).decode("utf-8")
            if ":" not in decoded:
                raise AuthNotFound("Basic")
            username, password = decoded.split(":", 1)
            return username, password
        except Exception:
            raise AuthNotFound("Basic")

    async def username(self) -> str:
        """Return Basic auth username or fail fast."""
        username, _ = await self.credentials()
        return username

    async def password(self) -> str:
        """Return Basic auth password or fail fast."""
        _, password = await self.credentials()
        return password

    async def has(self) -> bool:
        """Check if valid Basic authentication is present in request."""
        try:
            await self.credentials()
            return True
        except AuthNotFound:
            return False
