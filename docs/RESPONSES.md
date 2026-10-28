# HTTP Responses in `pyresponse`

> Pure OOP and Elegant Objects composable response guide.

In `pyresponse`, responses are not mutable dictionaries or procedural handler returns. Instead, every response is a composable domain object implementing the `Response` protocol:

```python
class Response(Protocol):
    def head(self) -> Head: ...
    async def body(self) -> AsyncIterable[bytes]: ...
```

By wrapping responses in decorators and envelopes, you construct clean, immutable, and testable HTTP responses.

---

## Table of Contents

1. [Status Codes](#1-status-codes)
2. [Payload Bodies (`Json`, `Text`, `Binary`)](#2-payload-bodies-json-text-binary)
3. [Server-Sent Events (SSE) & AI Streaming](#3-server-sent-events-sse--ai-streaming)
4. [Headers & Content Type](#4-headers--content-type)
5. [Cookies](#5-cookies)
6. [Caching & Performance](#6-caching--performance)
7. [Security Decorators](#7-security-decorators)
8. [Downloads & File Delivery](#8-downloads--file-delivery)
9. [Redirects](#9-redirects)
10. [Unit Testing Responses (Zero Network Overhead)](#10-unit-testing-responses-zero-network-overhead)

---

## 1. Status Codes

Use dedicated status decorators to define the HTTP status code:

```python
from pyresponse.response import BadRequest, Created, NoContent, NotFound, Ok, ServerError, StatusLine, Text

# Standard 200 OK
res = Ok(Text("All good"))

# 201 Created
res = Created(Text("Resource created"))

# 204 No Content (empty body)
res = NoContent()

# 400 Bad Request
res = BadRequest(Text("Invalid input"))

# 404 Not Found
res = NotFound(Text("Item not found"))

# 500 Internal Server Error
res = ServerError(Text("Something went wrong"))

# Custom Status Code
res = StatusLine(Text("I'm a teapot"), 418)
```

---

## 2. Payload Bodies (`Json`, `Text`, `Binary`)

Payload wrappers set appropriate `Content-Type` headers and format the body stream:

### JSON
Serializes Python dictionaries, lists, or primitives:
```python
from pyresponse.response import Json, Ok

response = Ok(Json({"id": 42, "name": "Alice", "tags": ["admin", "staff"]}))
```

### Text
Encodes text as UTF-8:
```python
from pyresponse.response import Ok, Text

response = Ok(Text("Hello, World!"))
```

### Binary
Streams raw bytes or binary generators (e.g. PDFs, images, generated audio):
```python
from pyresponse.response import Binary, Ok

pdf_bytes = b"%PDF-1.4 ..."
response = Ok(Binary(pdf_bytes, content_type="application/pdf"))
```

---

## 3. Server-Sent Events (SSE) & AI Streaming

`pyresponse` provides first-class OOP primitives for Server-Sent Events, ideal for AI token streaming (LLMs) and live updates:

```python
from collections.abc import AsyncIterable
from pyresponse.response import Event, Ok, Sse

async def token_generator() -> AsyncIterable[Event]:
    tokens = ["The ", "quick ", "brown ", "fox..."]
    for token in tokens:
        yield Event(data=token, name="token")
    yield Event(data="[DONE]", name="finish")

# Sse automatically configures:
# - Content-Type: text/event-stream
# - Cache-Control: no-cache
# - Connection: keep-alive
response = Ok(Sse(token_generator()))
```

`Event` supports:
- `data`: string payload
- `name`: event name (e.g. `event: message`)
- `id`: event identifier for replay
- `retry`: reconnect wait duration in milliseconds
- `comment`: SSE comment line (`: ping`)

---

## 4. Headers & Content Type

Decorate any response with headers without mutating original instances:

```python
from pyresponse.response import ContentType, Header, Ok, Text, WithoutHeader

# Add headers
res = Header(
    Header(Ok(Text("custom headers")), "X-Custom-Trace", "abc-123"),
    "X-Powered-By",
    "pyresponse",
)

# Explicit Content-Type decorator
res = ContentType(Ok(Text("<html><body>Hello</body></html>")), "text/html")

# Remove a header from an existing response envelope
clean_res = WithoutHeader(res, "X-Powered-By")
```

---

## 5. Cookies

Manage cookies declaratively using `Cookie`, `WithCookie`, and `WithoutCookie`:

```python
from pyresponse.response import Cookie, Ok, Text, WithCookie, WithoutCookie

# Set a cookie
res = WithCookie(
    Ok(Text("Logged in")),
    Cookie(
        name="session_id",
        value="secret-token-123",
        max_age=3600,
        http_only=True,
        secure=True,
        same_site="Lax",
        path="/",
    ),
)

# Expire / Delete a cookie
res_logout = WithoutCookie(Ok(Text("Logged out")), "session_id")
```

---

## 6. Caching & Performance

Add caching and compression decorators:

```python
from pyresponse.response import Cached, Etag, Gzip, NoCache, Ok, Text

# Cache for 1 hour (Cache-Control: public, max-age=3600)
cached_res = Cached(Ok(Text("cacheable content")), max_age=3600)

# Disable caching (Cache-Control: no-cache, no-store, must-revalidate)
fresh_res = NoCache(Ok(Text("realtime balance")))

# Attach ETag
tagged_res = Etag(Ok(Text("content")), '"v1.0.4"')

# Gzip compression (automatically compresses body and sets Content-Encoding: gzip)
compressed_res = Gzip(Ok(Text("large repetitive payload... " * 100)))
```

---

## 7. Security Decorators

Harden your application by composing standard security headers:

```python
from pyresponse.response import Cors, FrameOptions, Hsts, NoSniff, Ok, Secure, Text

# Secure wraps: NoSniff + FrameOptions(DENY) + Hsts
secure_res = Secure(Ok(Text("Protected content")))

# Or compose individually:
res = Hsts(
    FrameOptions(
        NoSniff(Ok(Text("Strict headers"))),
        mode="DENY",
    ),
    max_age=31536000,
    include_subdomains=True,
)

# CORS headers on response
cors_res = Cors(
    Ok(Text("CORS ready")),
    origins=("https://app.example.com",),
    methods=("GET", "POST"),
    headers=("Authorization", "Content-Type"),
)
```

---

## 8. Downloads & File Delivery

Force file downloads or inline browser rendering:

```python
from pyresponse.response import Attachment, Binary, Inline, Ok

# Prompt download: Content-Disposition: attachment; filename="report.pdf"
download_res = Attachment(
    Ok(Binary(b"...", content_type="application/pdf")),
    filename="financial-report.pdf",
)

# Display inline in browser: Content-Disposition: inline; filename="preview.png"
preview_res = Inline(
    Ok(Binary(b"...", content_type="image/png")),
    filename="preview.png",
)
```

---

## 9. Redirects

Create HTTP redirects with clean status codes (defaults to `307 Temporary Redirect`):

```python
from pyresponse.response import Redirect

# Temporary redirect
redirect_temp = Redirect("/dashboard")

# Permanent redirect
redirect_perm = Redirect("/new-url", status_code=308)
```

---

## 10. Unit Testing Responses & In-Memory ASGI (Zero Network Overhead)

Because responses and ASGI applications are pure domain objects, you can inspect and verify their status code, headers, and body directly in memory without starting any server or relying on `starlette.testclient.TestClient`:

```python
import pytest
from pyresponse import AsgiApp, Post, request
from pyresponse.request import WithBearerToken, WithJsonBody
from pyresponse.response import (
    Asgi as AsgiResponse,
    BodyBytes,
    BodyJson,
    BodyText,
    ExpectedBody,
    ExpectedHeader,
    ExpectedJson,
    ExpectedStatus,
    Json,
    Ok,
    Verified,
)

@pytest.mark.asyncio
async def test_in_memory_asgi_and_assertions():
    app = AsgiApp(
        Post("/api/chat", lambda req: Ok(Json({"status": "ok", "context_id": "ctx-123"})))
    )

    res = AsgiResponse(
        app,
        WithBearerToken(
            WithJsonBody(
                request.Fake(method="POST", path="/api/chat"),
                {"prompt": "Hello"},
            ),
            "token-123",
        ),
    )

    # 1. Inspect via focused response body inspectors:
    assert (await res.head()).status() == 200
    assert await BodyBytes(res).bytes() == b'{"status": "ok", "context_id": "ctx-123"}'
    assert "ctx-123" in await BodyText(res).text()
    assert (await BodyJson(res).value())["context_id"] == "ctx-123"

    # 2. Or verify declaratively (Tell, Don't Ask):
    await Verified(
        res,
        ExpectedStatus(200),
        ExpectedHeader("content-type", "application/json"),
        ExpectedBody("ctx-123"),
        ExpectedJson(("context_id",), "ctx-123"),
    ).verify()
```
