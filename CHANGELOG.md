# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2026-10-10

### Added
- Transparent empty path handling in `Path` routing fork to seamlessly support nested routes inside `Regex` and `Prefix`.
- Autonomous bash runner script `pyr` discovering local or parent virtual environments without requiring manual activation.

### Changed
- `ExitCode` subclasses `int` for zero-overhead OS exit code handling in CLI entry points without losing object-oriented semantics (`success()`, `failure()`, `terminate()`).
- Enforced 100% code-free constructors in response decorators `Cached` and `Hsts`, deferring header generation to `head()`.

### Removed
- Redundant CLI pseudo-package directory `pyr/`.

## [0.5.0] - 2026-10-10

### Added
- `ForkEnvelope` decorator pattern for router forks, delegating `matched()`, `routes()`, `route()`, and `response()`.
- Pure OOP CLI domain objects: `Arguments` (`ArgumentsFrom`, `SysArguments`, `ArgumentNotFound`) and `ExitCode` (`Success`, `Failure`), replacing primitive `list[str]` and `int`.
- `AppCommands` domain composite assembling application, discovered, and framework CLI commands without procedural list mutations.

### Changed
- Refactored `Cors` and `Trap` from inheriting `Fork` to pure `ForkEnvelope` decorators.
- Eliminated static factory tricks in `Fork` and removed `CompositeFork`.
- Enforced Elegant Objects naming conventions: removed all `is_` prefixes (`success()`, `failure()`, `empty()`) and abolished generic filler class names (`DefaultCommands`, `StandardCommands`).
- Replaced `isinstance` type inspections with polymorphism and duck typing across route discovery.
- Eliminated hidden getters like `__int__()` from `ExitCode` and dummy empty-string fallbacks from `RoutesCommand`.

## [0.4.0] - 2026-10-10

### Added
- Pure OOP Elegant Objects refactoring across entire codebase without regard for legacy constraints.
- 100% code-free constructors across all domain models and envelopes.
- Real domain null-objects and envelopes eliminating all `None` values and `None`-checks (`EmptyFork`, `MissingEndpoint`).
- Strict 200-line file length limit enforced repository-wide; extracted cohesive domain objects for CLI targets (`Coordinate`, `Directory`, `Candidate`, `Target`, `ExplicitTarget`, `InPathTarget`).
- Comprehensive HTTP response decorators: `Ok`, `Created`, `NoContent`, `BadRequest`, `NotFound`, `ServerError`, `StatusLine`, `Body`, `BytesBody`, `TextBody`, `StreamBody`, `Sse`, `Event`, `SseEvent`, `Secure`, `NoSniff`, `FrameOptions`, `Hsts`, `Cors`, `Cookie`, `WithCookie`, `WithoutCookie`, `Cached`, `NoCache`, `Etag`, `Gzip`, `Chunked`, `Attachment`, `Inline`, `Redirect`, `Location`, `RetryAfter`, `ServerTiming`.
- Comprehensive HTTP request inspectors and decorators: `Method`, `Path`, `QueryParams`, `PathParams`, `Cookies`, `Header`, `Host`, `UserAgent`, `Accept`, `ContentType`, `Authorization`, `BearerToken`, `BasicAuth`, `BodyBytes`, `Json`, `Urlencoded`, `Multipart`, `Fake`, and immutable `With*` request transformers.
- Advanced routing forks: `Route`, `Host` (virtual hosting), `HeaderFork` (header-based routing and API versioning), `GuardedEndpoint`, `GuardedBranch`, `MeasuredEndpoint`, `LoggedFork`.
- ASGI lifespan management objects: `Lifespan`, `Envelope`, `ForkLifespan`, `WithStartup`, `WithShutdown`.
- Extensive developer guides in `docs/RESPONSES.md`, `docs/REQUESTS.md`, and updated `docs/ROUTING.md`, `README.md`, `REQUIREMENTS.md`.

### Changed
- Standardized response class naming to PascalCase (e.g. `Ok` instead of procedural `OK`).
- Removed all private helper functions, methods, and classes (`_...`).

## [0.3.1] - 2026-10-10

### Changed
- Renamed CLI shortcut alias from `pr` to `pyr` to avoid collision with standard POSIX `/usr/bin/pr` utility.

## [0.3.0] - 2026-10-10

### Added
- Unified Pure OOP CLI framework with commands `pyresponse` and short alias `pr`.
- `pr routes` command for dynamic ASGI route inspection unwrapping `AsgiApp`, `Cors`, `Trap`, and custom routers.
- `pr serve` command with configurable port, host, reload, and auto-discovered targets.
- `pr help` menu displaying built-in and plugin commands.
- Dynamic plugin discovery via `pyresponse.commands` entry points (e.g. `pyaidoc` registering `pr ai:tools` and `pr ai:docs`).
- Comprehensive documentation in `docs/CLI.md` and updated `README.md`.

## [0.2.0] - 2026-10-09

### Added
- Pure OOP domain exception hierarchy (`Error`, `RouteNotFound`, `AuthNotFound`, `CookieNotFound`, `HeaderNotFound`, `ParamNotFound`, `FieldNotFound`).
- `Sticky` request decorator caching coroutine results in Pure OOP.
- CORS wrapper `Cors` and error handling `Trap`.

## [0.1.0] - 2026-10-08

### Added
- Pure OOP ASGI micro-framework adhering to Yegor Bugayenko's *Elegant Objects*.
- Autonomous request, response, and routing fork objects.
