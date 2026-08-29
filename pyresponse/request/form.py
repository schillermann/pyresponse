"""Multipart form data and file upload parsing."""

import io
from typing import Any
from pyresponse.request.request import Decorator, Request


class UploadFile:
    """Encapsulation of an uploaded multipart file."""

    def __init__(
        self,
        filename: str,
        content_type: str,
        content: bytes,
        headers: dict[str, str] = {},
    ) -> None:
        self._filename = filename
        self._content_type = content_type
        self._content = content
        self._headers = headers

    def filename(self) -> str:
        return self._filename

    def content_type(self) -> str:
        return self._content_type

    def headers(self) -> dict[str, str]:
        return self._headers

    async def read(self) -> bytes:
        return self._content

    def size(self) -> int:
        return len(self._content)


class FormData:
    """Parsed multipart / form data."""

    def __init__(
        self,
        fields: dict[str, list[str]] = {},
        files: dict[str, list[UploadFile]] = {},
    ) -> None:
        self._fields = fields
        self._files = files

    def field(self, name: str, default: str = "") -> str:
        if name in self._fields and self._fields[name]:
            return self._fields[name][0]
        return default

    def field_list(self, name: str) -> list[str]:
        return self._fields.get(name, [])

    def file(self, name: str) -> UploadFile | None:
        if name in self._files and self._files[name]:
            return self._files[name][0]
        return None

    def file_list(self, name: str) -> list[UploadFile]:
        return self._files.get(name, [])

    def fields(self) -> dict[str, list[str]]:
        return self._fields

    def files(self) -> dict[str, list[UploadFile]]:
        return self._files


class Multipart(Decorator):
    """Streaming multipart / form-data parser for file uploads and form fields."""

    async def form(self) -> FormData:
        chunks = []
        async for chunk in self._origin.body():
            chunks.append(chunk)
        raw_body = b"".join(chunks)

        header = await self._origin.head()
        content_type_header = header.as_string("content-type", default="")
        if not content_type_header:
            return FormData()

        fields: dict[str, list[str]] = {}
        files: dict[str, list[UploadFile]] = {}

        try:
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

                ct = "application/octet-stream"
                for h_name, h_val in getattr(file_obj, "headerlist", []):
                    h_n = (
                        h_name.decode("latin1").lower()
                        if isinstance(h_name, bytes)
                        else str(h_name).lower()
                    )
                    if h_n == "content-type":
                        ct = h_val.decode("latin1") if isinstance(h_val, bytes) else str(h_val)

                upload = UploadFile(filename=file_name, content_type=ct, content=content)
                files.setdefault(field_name, []).append(upload)

            multipart_mod.parse_form(
                headers=headers,
                input_stream=io.BytesIO(raw_body),
                on_field=on_field,
                on_file=on_file,
            )
        except Exception:
            pass

        return FormData(fields=fields, files=files)
