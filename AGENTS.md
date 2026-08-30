# AGENTS.md

Guidelines, architectural rules, and conventions for AI agents operating in the `pyresponse` codebase.

---

## 1. Git & Commit Guidelines

- **Staged Changes Focus**: Commit messages must always accurately describe the changes currently staged in `git diff --cached``git status`.
- **Conventional Commits v1.0.0 Compliance**:
  - Format: `<type>[optional scope]: <description>`
  - Types:
    - `feat`: New feature or capability
    - `fix`: Bug fix
    - `docs`: Documentation changes
    - `style`: Formatting, missing semicolons, etc. (no functional code changes)
    - `refactor`: Refactoring code without adding features or fixing bugs
    - `perf`: Performance improvements
    - `test`: Adding or updating tests
    - `build`: Build system or dependency updates
    - `ci`: CI configuration and script updates
    - `chore`: Maintenance tasks
  - Breaking Changes: Use `!` before `:` or `BREAKING CHANGE: <description>` in the footer.

---

## 2. Core Architecture & Philosophy (Elegant ObjectsPure OOP)

`pyresponse` follows strict **Elegant Objects** (Yegor Bugayenko) and pure Object-Oriented Programming (Alan KaySmalltalk) principles:

1. **No Annotations/Decorators as Route Endpoints**:
   - Never use procedural routing decorators like `@app.get(...)` or `@app.post(...)`.
   - Resources/endpoints are first-class domain objects (`Resource`) or functions receiving a `Request` and returning a `Response`.

2. **Composition over Inheritance (Decorator Pattern)**:
   - Build responses and behavior by wrapping domain objects in composable decorators.
   - Response decorators: `Body`, `Header`, `StatusLine`, `OK`, `Json`, `Text`, `Binary`, `Sse`, `Redirect`, `NoContent`, etc.
   - Request wrappers/inspectors: `Request`, `WithParams`, etc.

3. **100% Code-Free Constructors**:
   - `__init__` methods must strictly only perform attribute assignments (`self._param = param`).
   - No validation, conditionals, type conversions, side effects, or business logic inside `__init__`.

4. **Never Accept, Never Return `None` (Fail Fast & Explicit Domain Models)**:
   - Never return `None` or use `None` checks for missing values.
   - Use real domain entities (`NoContent`, `Body()`, `Lifespan()`) or fail fast with meaningful domain exceptions (`HeaderNotFound`, `RouteNotFound`, `ParamNotFound`).
   - Use fallback decorators or explicit defaults for optional values rather than dummy null objects.

5. **No GettersSettersAnemic DTOs**:
   - Do not create anemic data structures with getter/setter methods.
   - Encapsulate data and behavior together within cohesive domain objects.

6. **No Static Methods & No Global Singletons**:
   - Avoid global mutable state, singleton app containers, and `@staticmethod``@classmethod` utility dumps.
   - Explicitly construct and compose dependencies at the composition root.

---

## 3. Technology Stack & Standards

- **Language**: Python >= 3.11
- **Specification**: ASGI 3.0 (`http` scope and `lifespan` events)
- **Testing**: `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`, tests placed in `tests/`)
- **Documentation**: Keep `README.md` and `REQUIREMENTS.md` aligned with any architectural additions.
