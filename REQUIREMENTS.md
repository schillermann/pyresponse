# Requirements Specification: `pyresponse`

> **A Pure OOP / Elegant Objects ASGI Web Framework for Python**  
> Tailored for high-performance enterprise applications, AI streaming, and zero-annotation architectures.

---

## 1. Architectural Philosophy (Elegant Objects / Yegor Bugayenko)

`pyresponse` is built strictly according to **Yegor Bugayenko's Elegant Objects** principles:

1. **No Annotations/Decorators as Route Handlers**:
   - No `@app.get(...)` or `@app.post(...)`.
   - Handlers are first-class domain objects implementing the `Take` interface (`take(req) -> res`).
2. **Composition & Decorator Pattern**:
   - Requests and responses are wrapped in composable decorators (`RsWithStatus`, `RsWithHeader`, `RsJson`, `RqHeader`, `RqJson`).
   - Routing is a tree of fork decorators (`TkFork`, `FkRegex`, `FkMethod`).
3. **100% Code-Free Constructors**:
   - Constructors only perform parameter assignments (`self._param = param`).
   - No business logic, validation, network calls, or conditionals inside `__init__`.
4. **Never Return `None` (Null Object Pattern)**:
   - Queries return polymorphic Null Objects (`NoHeader`, `EmptyBody`, `NoUser`, `AnonymousSession`) rather than `None` or raising control-flow exceptions.
5. **No Getters / Setters / Anemic DTOs**:
   - Encapsulate data and behavior together.
6. **No Static Methods / No Global Singletons**:
   - Composition root handles dependency injection explicitly.

---

## 2. Core Protocol & Framework Requirements

### 2.1 ASGI 3.0 Compliance
- Implementation of `AsgiApp` compatible with standard ASGI servers (`uvicorn`, `granian`, `hypercorn`).
- Support for `http` connection scope and `lifespan` protocol (`lifespan.startup`, `lifespan.shutdown`) to manage async database pools and external services.

### 2.2 Core Interfaces
- **`Request`**:
  - `head()`: Provides metadata (method, URI path, query strings, headers).
  - `body()`: Provides an async byte stream of the request payload.
- **`Response`**:
  - `head()`: Provides HTTP status code and response headers.
  - `body()`: Provides an async byte stream / generator for sending data.
- **`Take`**:
  - `async def take(self, request: Request) -> Response`
- **`Fork`**:
  - Evaluates whether a request matches criteria and routes to a targeted `Take`.

### 2.3 Request Decorators
- `RqMethod`: HTTP method query (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`).
- `RqPath`: Path string query.
- `RqHeader`: Header lookup by key, returning `NoHeader` when missing.
- `RqQueryParams`: Query string parser for structured search and pagination.
- `RqPathParams`: Regex path variable extractor (e.g. `/api/documents/(?P<doc_id>[a-zA-Z0-9_-]+)`).
- `RqJson`: Async payload reader deserializing JSON into domain entities.
- `RqMultipart` / `RqFormData`: Streaming multipart parser for file uploads (PDF, audio, documents).

### 2.4 Response Decorators
- `RsWithStatus(response, status_code)`: Wraps status code (200, 201, 400, 401, 403, 404, 500, etc.).
- `RsWithHeader(response, key, value)`: Attaches HTTP headers.
- `RsJson(domain_object)`: Serializes domain models/dictionaries to JSON.
- `RsText(text)`: Plain text response.
- `RsBinary(stream, content_type)`: Binary file streaming (for downloads and PDF viewing).
- `RsSse(async_event_stream)`: **Server-Sent Events (SSE)** response generator emitting `event: ...\ndata: ...\n\n` for AI token streaming.
- `RsEmpty()`: 204 No Content response.
- `RsRedirect(target_url, status_code=307)`: HTTP redirect.

### 2.5 Routing & Middleware (Takes & Forks)
- `TkFork`: Master router evaluating a collection of `Fork` instances in sequence.
- `FkRegex`: Regex URI matcher.
- `FkMethod`: HTTP method filter.
- `TkCors`: CORS decorator with origin, header, method, and preflight (`OPTIONS`) handling.
- `TkSafe` / `TkFallback`: Error boundary decorator catching unhandled exceptions and returning structured JSON errors.
- `TkAuth`: Authentication and tenancy interceptor passing authenticated context to inner takes.

---

## 3. Compatibility Requirements

To serve as a full replacement for FastAPI, `pyresponse` must support:

| Feature | Required Framework Support |
| :--- | :--- |
| **Realtime AI Streaming** (`/api/chat/stream`) | Async SSE response decorator (`RsSse`), token stream generators, non-blocking I/O |
| **Fast-Path Engine (<10ms)** | Low-overhead routing (`TkFork` / `FkRegex`), zero reflection/inspection penalty |
| **Document Uploads** (`/api/documents/upload`) | Async `multipart/form-data` stream parser (`RqMultipart`), S3 streaming |
| **Audio Dictation** (`/api/audio/transcribe`) | Multipart audio payload parsing, streaming bytes to `faster-whisper` |
| **Document Downloads** (`/api/documents/{id}/download`) | `RsBinary` with `Content-Disposition: inline` / `attachment` and MIME detection |
| **Template Processing** (`/api/templates/*`) | File uploads and generated PDF/Word binary streaming |
| **Multi-Tenancy & Auth** | Context propagation via decorators (`TkAuth`, `X-User-Id`, `X-Tenant-Id`) |
| **Database Pool Lifespan** | ASGI lifespan startup/shutdown handling for `asyncpg` pools |
| **Frontend Compatibility** | 100% JSON & SSE protocol contract compatibility with Vite frontend |
