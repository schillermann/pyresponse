# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
