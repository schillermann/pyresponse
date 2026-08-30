"""HTTP Basic authentication extractor."""

import base64
from pyresponse.request.auth_not_found import AuthNotFoundError
from pyresponse.request.envelope import Envelope
from pyresponse.request.request import Request


class BasicAuth(Envelope):
    """Decorator extracting Basic authentication username and password from Authorization header."""

    async def credentials(self) -> tuple[str, str]:
        """Extract and return (username, password) tuple or fail fast with AuthNotFoundError."""
        head = await self._origin.head()
        raw_auth = head.value_or("authorization", "").strip()
        if not raw_auth:
            raise AuthNotFoundError("Basic")
        parts = raw_auth.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "basic":
            raise AuthNotFoundError("Basic")
        try:
            decoded = base64.b64decode(parts[1].strip()).decode("utf-8")
            if ":" not in decoded:
                raise AuthNotFoundError("Basic")
            username, password = decoded.split(":", 1)
            return username, password
        except Exception:
            raise AuthNotFoundError("Basic")

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
        except AuthNotFoundError:
            return False
