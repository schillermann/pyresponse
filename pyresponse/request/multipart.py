"""Streaming multipart / form-data parser."""

import io
from typing import Any

from pyresponse.request.envelope import Envelope
from pyresponse.request.files import Files
from pyresponse.request.form import Form
from pyresponse.request.head import Head
from pyresponse.request.upload_file import UploadFile


class Multipart(Envelope):
    """Streaming multipart / form-data parser for file uploads and form fields."""

    async def _parse(self) -> tuple[Form, Files]:
        chunks = []
        async for chunk in self._origin.body():
            chunks.append(chunk)
        raw_body = b"".join(chunks)

        header = await self._origin.head()
        content_type_header = header.value_or("content-type", "")
        if not content_type_header:
            return Form(), Files()

        fields: dict[str, list[str]] = {}
        files: dict[str, list[UploadFile]] = {}

        try:
            import python_multipart as multipart_mod
        except ImportError:
            import multipart as multipart_mod

        headers = {"Content-Type": content_type_header.encode("latin1")}

        def on_field(field_obj: Any) -> None:
            name = (
                field_obj.field_name.decode("utf-8", errors="replace")
                if isinstance(field_obj.field_name, bytes)
                else str(field_obj.field_name)
            )
            val = (
                field_obj.value.decode("utf-8", errors="replace")
                if isinstance(field_obj.value, bytes)
                else str(field_obj.value)
            )
            fields.setdefault(name, []).append(val)

        def on_file(file_obj: Any) -> None:
            field_name = (
                file_obj.field_name.decode("utf-8", errors="replace")
                if isinstance(file_obj.field_name, bytes)
                else str(file_obj.field_name)
            )
            file_name = (
                file_obj.file_name.decode("utf-8", errors="replace")
                if isinstance(file_obj.file_name, bytes)
                else (str(file_obj.file_name) if file_obj.file_name else "")
            )

            file_obj.file_object.seek(0)
            content = file_obj.file_object.read()

            raw_ct = getattr(file_obj, "content_type", "")
            if isinstance(raw_ct, bytes):
                ct = raw_ct.decode("latin1")
            elif raw_ct:
                ct = str(raw_ct)
            else:
                ct = "application/octet-stream"

            part_headers: list[tuple[bytes, bytes]] = [
                (b"content-type", ct.encode("latin1")),
            ]
            if file_name:
                part_headers.append(
                    (b"content-disposition", f'form-data; name="{field_name}"; filename="{file_name}"'.encode("latin1"))
                )

            upload = UploadFile(
                filename=file_name,
                content_type=ct,
                content=content,
                head=Head(part_headers),
            )
            files.setdefault(field_name, []).append(upload)

        multipart_mod.parse_form(
            headers=headers,
            input_stream=io.BytesIO(raw_body),
            on_field=on_field,
            on_file=on_file,
        )

        return Form(fields=fields), Files(files=files)

    async def form(self) -> Form:
        """Parse request body and return Form domain object for text parameters."""
        form, _ = await self._parse()
        return form

    async def files(self) -> Files:
        """Parse request body and return Files domain object for uploaded files."""
        _, files = await self._parse()
        return files

    async def field(self, name: str) -> str:
        """Return single field value or fail fast with FieldNotFoundError."""
        form = await self.form()
        return form.field(name)

    async def file(self, name: str) -> UploadFile:
        """Return uploaded file or fail fast with UploadNotFoundError."""
        files = await self.files()
        return files.file(name)

    async def has(self, name: str) -> bool:
        """Check if form field is present."""
        form = await self.form()
        return form.has(name)

    async def has_file(self, name: str) -> bool:
        """Check if uploaded file is present."""
        files = await self.files()
        return files.has(name)



