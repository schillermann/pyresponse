# AGENTS.md

Guidelines, architectural rules, and conventions for AI agents operating in the `pyresponse` codebase.

---

## 1. Git & Commit Guidelines

- **Staged Changes Focus**: Commit messages must always accurately describe the changes currently staged in `git diff --cached` / `git status`.
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

## 2. Core Architecture & Philosophy (Elegant Objects / Pure OOP)

`pyresponse` follows strict **Elegant Objects** (Yegor Bugayenko) and pure Object-Oriented Programming (Alan Kay / Smalltalk / Takes / Cactoos) principles:

1. **No Annotations/Decorators as Route Handlers**:
   - Never use procedural routing decorators like `@app.get(...)` or `@app.post(...)`.
   - Handlers are first-class domain objects implementing the `Take` interface (`async def take(self, request: Request) -> Response`).

2. **Composition over Inheritance (Decorator Pattern)**:
   - Build functionality by wrapping objects in composable decorators.
   - Request decorators: `RqMethod`, `RqPath`, `RqHeader`, `RqQueryParams`, `RqPathParams`, `RqJson`, `RqMultipart`, etc.
   - Response decorators: `RsWithStatus`, `RsWithHeader`, `RsJson`, `RsText`, `RsBinary`, `RsSse`, `RsEmpty`, `RsRedirect`, etc.
   - Routing: Composed fork trees (`TkFork`, `FkRegex`, `FkMethod`).

3. **100% Code-Free Constructors**:
   - `__init__` methods must strictly only perform attribute assignments (`self._param = param`).
   - No validation, conditionals, type conversions, side effects, or business logic inside `__init__`.

4. **Never Return `None` (Null Object Pattern)**:
   - Do not return `None` or use `None` checks for missing values.
   - Use polymorphic Null Objects (e.g., `NoHeader`, `EmptyBody`, `NoUser`, `AnonymousSession`).

5. **No Getters / Setters / Anemic DTOs**:
   - Do not create anemic data structures with getter/setter methods.
   - Encapsulate data and behavior together within cohesive domain objects.

6. **No Static Methods & No Global Singletons**:
   - Avoid global mutable state, singleton app containers, and `@staticmethod` / `@classmethod` utility dumps.
   - Explicitly construct and compose dependencies at the composition root.

---

## 3. Technology Stack & Standards

- **Language**: Python >= 3.11
- **Specification**: ASGI 3.0 (`http` scope and `lifespan` events)
- **Testing**: `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`, tests placed in `tests/`)
- **Documentation**: Keep `README.md` and `REQUIREMENTS.md` aligned with any architectural additions.
