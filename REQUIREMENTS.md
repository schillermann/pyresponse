# Requirements Specification: `pyresponse`

> **A Pure OOP / Elegant Objects ASGI Web Framework for Python**  
> Tailored for high-performance enterprise applications, AI streaming, and zero-annotation architectures.

---

## 1. Architectural Philosophy (Elegant Objects / Yegor Bugayenko)

`pyresponse` is built strictly according to **Yegor Bugayenko's Elegant Objects** principles:

1. **No Annotations/Decorators as Route Handlers**:
   - No `@app.get(...)` or `@app.post(...)`.
   - Handlers are first-class domain objects or functions receiving a `Request` and returning a `Response`.
2. **Composition & Envelope Pattern**:
   - Responses are composed by wrapping domain objects in composable decorators/envelopes (`Body`, `Header`, `StatusLine`, `Ok`, `Json`, `Text`, `Binary`, `Sse`, `Redirect`, `NoContent`, `ResponseEnvelope`).
   - Requests provide composable inspection and streaming extraction (`Method`, `Path`, `Header`, `QueryParams`, `PathParams`, `Json`, `Multipart`, `Form`, `RequestEnvelope`).
   - Routing is built with composable forks (`Fork`, `Path`, `Regex`, `Method`, `Prefix`, `Trap`, `Host`, `HeaderFork`).
3. **1-Class = 1-File Strict Modularity**:
   - Every domain object, exception, and protocol lives in its own dedicated source file.
4. **100% Code-Free Constructors**:
   - Constructors strictly perform attribute assignments (`self._param = param`).
   - No business logic, validation, network calls, or conditionals inside `__init__`.
   - Default collections are strictly immutable (`MappingProxyType({})`, `()`).
5. **Never Accept, Never Return `None` (Fail Fast & Explicit Domain Models)**:
   - Never return `None` or use `None` checks for missing values.
   - Use real domain entities (`NoContent`, `Body()`, `Lifespan()`) or fail fast with meaningful domain exceptions (`HeaderNotFound`, `RouteNotFound`, `ParamNotFound`).
   - Use fallback decorators or explicit defaults for optional values rather than dummy null objects.
6. **No Getters / Setters / Anemic DTOs**:
   - Encapsulate data and behavior together within cohesive domain models.
7. **No Static Methods / No Global Singletons**:
   - Composition root handles dependency injection explicitly.
8. **File Length Limit (Max 200 Lines)**:
   - Every code file strictly does not exceed 200 lines to maintain cohesion and prevent monster objects.

---

## 2. Core Protocol & Framework Requirements

### 2.1 ASGI 3.0 Compliance
- Implementation of `AsgiApp` compatible with standard ASGI servers (`uvicorn`, `granian`, `hypercorn`).
- Support for `http` connection scope and `lifespan` protocol (`lifespan.startup`, `lifespan.shutdown`) to manage async database pools and external services.

### 2.2 Core Interfaces
- **`Request`**:
  - `head()`: Provides request head encapsulation (`Head`).
  - `method()`: Provides HTTP method string.
  - `path()`: Provides URI path string.
  - `query_string()`: Provides raw query bytes.
  - `path_params()`: Provides extracted route path parameters.
  - `body()`: Provides an async byte stream of the request payload.
- **`Response`**:
  - `head()`: Provides HTTP status code and response headers.
  - `body()`: Provides an async byte stream generator for sending data.
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
- `Header`: Header lookup by key, failing fast with `HeaderNotFound` when missing without default.
- `Host`: HTTP Host header inspector.
- `UserAgent`: User-Agent header inspector.
- `Accept`: Accept header inspector.
- `ContentType`: Content-Type header inspector.
- `Authorization`: Raw Authorization header inspector.
- `BearerToken`: Extracted Bearer token inspector.
- `BasicAuth`: HTTP Basic authentication username/password extractor.
- `Cookies`: Parsed request cookies inspector.
- `QueryParams`: Query string parser for structured search and pagination.
- `PathParams`: Regex path variable extractor (e.g. `/api/documents/(?P<doc_id>[a-zA-Z0-9_-]+)`).
- `BodyBytes`: Async payload reader returning full body as bytes.
- `Json`: Async payload reader deserializing JSON into domain entities.
- `Urlencoded`: Async parser for `application/x-www-form-urlencoded` forms.
- `Multipart`: Streaming multipart parser for file uploads (PDF, audio, documents).
- Request mutation envelopes: `WithMethod`, `WithPath`, `WithHeader`, `WithoutHeader`, `WithQuery`, `WithQueryParam`, `WithoutQueryParam`, `WithCookie`, `WithBody`, `WithJsonBody`, `WithBearerToken`, `WithBasicAuth`, `WithUserAgent`, `WithAccept`, `WithParams`.

### 2.4 Response Decorators
- `StatusLine(response, status_code)`: Wraps status code (200, 201, 400, 401, 403, 404, 500, etc.).
- `Ok`, `Created`, `NoContent`, `BadRequest`, `NotFound`, `ServerError`: Dedicated status code wrappers.
- `Header(response, key, value)`: Attaches HTTP headers.
- `WithoutHeader(response, key)`: Drops HTTP headers from response.
- `ContentType(response, mime)`: Sets `Content-Type`.
- `Body(content)`, `BytesBody(bytes)`, `TextBody(str)`, `StreamBody(stream)`, `WithBody(response, body)`: Encapsulates response payload body.
- `Json(domain_object)`: Serializes domain models/dictionaries to JSON.
- `Text(text)`: Plain text response.
- `Binary(stream, content_type)`: Binary file streaming (for downloads and PDF viewing).
- `Sse(async_event_stream)`, `Event`, `SseEvent`: **Server-Sent Events (SSE)** response generator emitting `event: ...\ndata: ...\n\n` for AI token streaming.
- `Cookie`, `WithCookie`, `WithoutCookie`: Declarative cookie manipulation.
- `Cached(response, max_age)`, `NoCache(response)`, `Etag(response, tag)`: HTTP cache control.
- `Gzip(response)`: On-the-fly Gzip compression.
- `Chunked(response)`: Chunked transfer encoding.
- `Secure(response)`, `Hsts`, `NoSniff`, `FrameOptions`: HTTP security headers.
- `Cors(response, origins, methods, headers)`: Response-level CORS headers.
- `Attachment(response, filename)`, `Inline(response, filename)`: Content-Disposition headers.
- `Redirect(target_url, status_code=307)`, `Location(response, url)`: HTTP redirect.
- `RetryAfter(response, seconds)`: Retry-After header.
- `ServerTiming(response, metric)`: Server-Timing performance header.

### 2.5 Routing & Forks
- `Fork`: Composite fork evaluating a sequence of branch forks.
- `EmptyFork`: Null-object fork that never matches.
- `Route`: Direct HTTP method and path pairing with an endpoint.
- `Path`: Exact URI path matcher fork.
- `SubPath`, `Prefix`: URI path prefix matcher fork for mounting sub-routers.
- `Regex`: Regex URI matcher with parameter extraction fork.
- `Method`: HTTP method filter fork.
- `Get`, `Post`, `Put`, `Delete`, `Patch`, `Options`, `Head`: Composable HTTP method-specific routing forks.
- `Host`: Virtual host routing fork by domain / hostname.
- `HeaderFork`: Header-based routing fork (API versioning / content negotiation).
- `GuardedEndpoint`, `GuardedBranch`: Conditional endpoint protection based on request predicate.
- `MeasuredEndpoint`, `LoggedFork`: Diagnostic metrics and logging for routes.
- `ForkEnvelope`: Base decorator pattern for router forks, delegating matched, routes, route, and response.
- `Cors`: Route-level CORS handling for preflight and actual requests (decorating `ForkEnvelope`).
- `Trap`: Exception trapping decorator converting domain errors to HTTP error responses (decorating `ForkEnvelope`).
- `Fallback`: Fallback endpoint decorator when no child branch matches.

### 2.6 Lifespan Management
- `Lifespan`: Core protocol for `startup()` and `shutdown()`.
- `ForkLifespan`: Composite lifespan dispatching lifecycle events across multiple services.
- `WithStartup`, `WithShutdown`: Decorators attaching startup/shutdown hooks.

### 2.7 Developer Console & CLI (`pyresponse.cli`)
- `Arguments`: CLI arguments domain object (`Arguments`, `ArgumentsFrom`, `SysArguments`), replacing primitive `list[str]`.
- `ExitCode`: Process termination domain object (`ExitCode`, `Success`, `Failure`), replacing primitive `int`.
- `CliCommand`: Protocol defining autonomous console commands (`name()`, `description()`, `matches(verb)`, `execute(args: Arguments) -> ExitCode`).
- `ForkCli`: Composite command router dispatching verbs to matching commands without procedural branching.
- `ServeCommand`: Command starting the development ASGI server via Uvicorn with auto-reload.
- `RoutesCommand`: Command inspecting `Fork` router trees and rendering formatted route tables via `SourceRoutes` and `RoutesTable`.
- `HelpCommand`: Interactive and searchable help display.
- `DiscoveredCommands`: Discovery decorator loading external commands registered via entry point group `pyresponse.commands`.
- `AppCommands`: Composite application commands assembling user-defined, auto-discovered, and framework CLI commands.
- `CliApp`: Autonomous composite CLI runner executing commands.

---

## 3. Compatibility Requirements

To serve as a full replacement for FastAPI, `pyresponse` must support:

| Feature | Required Framework Support |
| :--- | :--- |
| **Realtime AI Streaming** (`/api/chat/stream`) | Async SSE response decorator (`Sse`, `Event`), token stream generators, non-blocking I/O |
| **Fast-Path Engine (<10ms)** | Low-overhead fork routing (`Fork`, `Regex`, `Route`), zero reflection/inspection penalty |
| **Document Uploads** (`/api/documents/upload`) | Async `multipart/form-data` stream parser (`Multipart`), S3 streaming |
| **Audio Dictation** (`/api/audio/transcribe`) | Multipart audio payload parsing, streaming bytes to `faster-whisper` |
| **Document Downloads** (`/api/documents/{id}/download`) | `Binary` with `Content-Disposition: inline` / `attachment` and MIME detection |
| **Template Processing** (`/api/templates/*`) | File uploads and generated PDF/Word binary streaming |
| **Multi-Tenancy & Auth** | Host routing (`Host`), token extraction (`BearerToken`, `BasicAuth`), context propagation via request decorators |
| **Database Pool Lifespan** | ASGI lifespan startup/shutdown handling (`ForkLifespan`) for `asyncpg` pools |
| **Frontend Compatibility** | 100% JSON & SSE protocol contract compatibility with Vite frontend |
