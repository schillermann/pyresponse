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

- **`create git message` Workflow & Pre-Commit Protocol**:
  - When the user prompts `create git message` (or asks to generate/prepare a commit message):
    1. **Type Checking (`pyright`)**: Run `pyright` strictly from the project's virtual environment (`.venv/bin/pyright <modified_python_files>`) on the modified/staged Python files only. Never use a global or external instance.
    2. **Fix Type Errors**: Resolve all errors identified by `pyright` immediately.
    3. **Run Tests**: Execute `pytest` (e.g. `.venv/bin/pytest`) to guarantee all tests pass.
    4. **Bump Version**: Increment the version number according to Semantic Versioning (`MAJOR.MINOR.PATCH`) across:
       - `pyproject.toml` (`version = "..."`)
       - `pyresponse/__init__.py` (`__version__ = "..."`)
       - `tests/test_domain_objects.py` (`assert pyresponse.__version__ == "..."`)
       - `CHANGELOG.md` (add `## [x.y.z] - YYYY-MM-DD`)
    5. **Generate Commit Message**: Propose or generate the Conventional Commit message reflecting the staged changes.

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

7. **File Length Limit (Max 200 Lines)**:
   - Code files must strictly not exceed 200 lines.
   - Keep classes and modules small, focused, and cohesive. Extract separate cohesive domain objects or split test modules whenever a file approaches or exceeds 200 lines.

---

## 3. Technology Stack & Standards

- **Language**: Python >= 3.11
- **Specification**: ASGI 3.0 (`http` scope and `lifespan` events)
- **Testing**: `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`, tests placed in `tests/`)
- **Documentation**: Keep `README.md` and `REQUIREMENTS.md` aligned with any architectural additions.
