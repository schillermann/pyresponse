from pyresponse.request.envelope import Envelope
from pyresponse.request.files import Files
from pyresponse.request.form import Form
from pyresponse.request.multipart import Multipart
from pyresponse.request.upload_file import UploadFile
from pyresponse.request.urlencoded import UrlEncoded


class RequestForm(Envelope):
    """Request envelope automatically parsing URL-encoded or multipart form data."""

    async def form(self) -> Form:
        """Parse request body as multipart or URL-encoded form based on Content-Type."""
        head = await self._origin.head()
        ct = head.value_or("content-type", "").lower()
        if "multipart/form-data" in ct:
            return await Multipart(self._origin).form()
        return await UrlEncoded(self._origin).form()

    async def files(self) -> Files:
        """Parse request body and return uploaded files domain object."""
        head = await self._origin.head()
        ct = head.value_or("content-type", "").lower()
        if "multipart/form-data" in ct:
            return await Multipart(self._origin).files()
        return Files()

    async def field(self, name: str) -> str:
        """Return single field value or fail fast with FieldNotFound."""
        f = await self.form()
        return f.field(name)

    async def file(self, name: str) -> UploadFile:
        """Return uploaded file or fail fast with UploadNotFound."""
        files = await self.files()
        return files.file(name)

    async def has(self, name: str) -> bool:
        """Check if form field is present."""
        f = await self.form()
        return f.has(name)

    async def has_file(self, name: str) -> bool:
        """Check if uploaded file is present."""
        files = await self.files()
        return files.has(name)
