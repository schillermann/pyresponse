# Requirements Specification: `pyresponse`

> **A Pure OOP / Elegant Objects ASGI Web Framework for Python**  
> Tailored for high-performance enterprise applications, AI streaming, and zero-annotation architectures.

---

## 1. Architectural Philosophy (Elegant Objects / Yegor Bugayenko)

`pyresponse` is built strictly according to **Yegor Bugayenko's Elegant Objects** principles:

1. **No Annotations/Decorators as Route Handlers**:
   - No `@app.get(...)` or `@app.post(...)`.
   - Handlers are first-class domain objects or functions receiving a `Request` and returning a `Response`.
2. **Composition & Decorator Pattern**:
   - Responses are composed by wrapping domain objects in composable decorators (`Body`, `Header`, `StatusLine`, `OK`, `Json`, `Text`, `Binary`, `Sse`, `Redirect`, `NoContent`).
   - Requests provide composable inspection and streaming extraction (`Method`, `Path`, `Header`, `QueryParams`, `PathParams`, `Json`, `Multipart`).
   - Routing is built with composable forks (`Fork`, `Path`, `Regex`, `Method`).
3. **100% Code-Free Constructors**:
   - Constructors only perform parameter assignments (`self._param = param`).
   - No business logic, validation, network calls, or conditionals inside `__init__`.
4. **Never Accept, Never Return `None` (Fail Fast & Explicit Domain Models)**:
   - Never return `None` or use `None` checks for missing values.
   - Use real domain entities (`NoContent`, `Body()`, `Lifespan()`) or fail fast with meaningful domain exceptions (`HeaderNotFoundError`, `RouteNotFoundError`, `ParamNotFoundError`).
   - Use fallback decorators or explicit defaults for optional values rather than dummy null objects.
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
  - `head()`: Provides header encapsulation (`Header`).
  - `method()`: Provides HTTP method string.
  - `path()`: Provides URI path string.
  - `query_string()`: Provides raw query bytes.
  - `path_params()`: Provides extracted route path parameters.
  - `body()`: Provides an async byte stream of the request payload.
- **`Response`**:
  - `head()`: Provides HTTP status code and response headers.
  - `body()`: Provides an async byte stream / generator for sending data.
- **`Endpoint`**:
  - `async def response(self, request: Request) -> Response`
- **`Fork`**:
  - `async def route(self, request: Request) -> Endpoint`
- **`Lifespan`**:
  - `async def startup(self) -> None`
  - `async def shutdown(self) -> None`

### 2.3 Request Decorators & Inspectors
- `Method`: HTTP method inspector (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`).
- `Path`: Path string inspector.
- `Header`: Header lookup by key, failing fast with `HeaderNotFoundError` when missing without default.
- `QueryParams`: Query string parser for structured search and pagination.
- `PathParams`: Regex path variable extractor (e.g. `/api/documents/(?P<doc_id>[a-zA-Z0-9_-]+)`).
- `Json`: Async payload reader deserializing JSON into domain entities.
- `Multipart`: Streaming multipart parser for file uploads (PDF, audio, documents).

### 2.4 Response Decorators
- `StatusLine(response, status_code)`: Wraps status code (200, 201, 400, 401, 403, 404, 500, etc.).
- `Ok(response)`: Wraps 200 OK status code.
- `Header(response, key, value)`: Attaches HTTP headers.
- `Body(content)`: Encapsulates response payload body.
- `Json(domain_object)`: Serializes domain models/dictionaries to JSON.
- `Text(text)`: Plain text response.
- `Binary(stream, content_type)`: Binary file streaming (for downloads and PDF viewing).
- `Sse(async_event_stream)`: **Server-Sent Events (SSE)** response generator emitting `event: ...\ndata: ...\n\n` for AI token streaming.
- `NoContent()`: 204 No Content response.
- `Redirect(target_url, status_code=307)`: HTTP redirect.

### 2.5 Routing & Forks
- `Fork`: Composite fork evaluating a sequence of branch forks.
- `Path`: Exact URI path matcher fork.
- `Regex`: Regex URI matcher with parameter extraction fork.
- `Method`: HTTP method filter fork.

---

## 3. Compatibility Requirements

To serve as a full replacement for FastAPI, `pyresponse` must support:

| Feature | Required Framework Support |
| :--- | :--- |
| **Realtime AI Streaming** (`/api/chat/stream`) | Async SSE response decorator (`ResponseSse`), token stream generators, non-blocking I/O |
| **Fast-Path Engine (<10ms)** | Low-overhead fork routing (`Fork` / `Regex`), zero reflection/inspection penalty |
| **Document Uploads** (`/api/documents/upload`) | Async `multipart/form-data` stream parser (`RequestMultipart`), S3 streaming |
| **Audio Dictation** (`/api/audio/transcribe`) | Multipart audio payload parsing, streaming bytes to `faster-whisper` |
| **Document Downloads** (`/api/documents/{id}/download`) | `ResponseBinary` with `Content-Disposition: inline` / `attachment` and MIME detection |
| **Template Processing** (`/api/templates/*`) | File uploads and generated PDF/Word binary streaming |
| **Multi-Tenancy & Auth** | Context propagation via request decorators |
| **Database Pool Lifespan** | ASGI lifespan startup/shutdown handling for `asyncpg` pools |
| **Frontend Compatibility** | 100% JSON & SSE protocol contract compatibility with Vite frontend |
