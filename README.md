# pyresponse

A simple web framework in Python that respects OOP.

Inspired by pure OOP, Alan Kay with [Smalltalk](https://en.wikipedia.org/wiki/Smalltalk), and Yegor Bugayenko's [*Elegant Objects*](https://www.elegantobjects.org/), [Cactoos](https://github.com/yegor256/cactoos), and [Takes](https://github.com/yegor256/takes).

I’ve also created the web framework in other languages that you can check out:
- [Java](https://github.com/schillermann/jresponses)
- [JavaScript](https://github.com/schillermann/jsresponses)
- [PhpResponse](https://github.com/schillermann/phpresponse)

---

## 🚀 Quick Start

### Installation

```bash
pip install pyresponse
```

### Example: Hello World

```python
from pyresponse import Server
from pyresponse.response import Ok, Text

Server(
    lambda request: Ok(Text("<h1>Hello from PyResponse!</h1>")),
    port=8000,
).start()
```

### Example: Composed Routing

```python
from pyresponse import Fork, Get, Json, Ok, Post, Route, Server, Text

app = Fork(
    Route("GET", "/", lambda req: Ok(Text("Welcome to PyResponse!"))),
    Get("/api/items", lambda req: Ok(Json([{"id": 1, "title": "First Item"}]))),
)

if __name__ == "__main__":
    Server(app, port=8000).start()
```

---

## 🛠️ CLI Usage

`pyresponse` includes an extensible, Pure OOP developer console available via `pyresponse` or the short alias `pyr`:

### Inspect Routes
```bash
pyr routes
# Lists all registered HTTP endpoints in a clean ANSI table
```

### Start Development Server
```bash
pyr serve
# Or specify a custom entrypoint:
pyr serve main:app
```

### Help Menu
```bash
pyr help
# Displays all built-in commands and installed plugin commands
```

### Ecosystem & Plugins
Commands from installed extensions (e.g. [pyaidoc](https://github.com/schillermann/pyaidoc)) are discovered automatically via Python entry points:
```bash
pyr ai:tools   # Inspect AI agent function calls and parameters
pyr ai:docs    # Generate standalone HTML AI reference documentation
```

For custom command creation, see the [Developer Console & CLI Guide](docs/CLI.md).

---

## 🎯 Motivation & Philosophy

Most modern Python web frameworks (FastAPI, Flask, Django) heavily rely on:
- Global state and singletons (`app = FastAPI()`, global dependency containers)
- Procedural routing decorators (`@app.get(...)`, `@app.post(...)`)
- Anemic data structures (DTOs with getters/setters or raw dictionaries)
- Reflection-based magic dependency injection

## Core Principles (Elegant Objects)
- **Strictly OOP**: No getters, no setters, no nulls.
- **Composition over Inheritance**: Functionality is built by composing decorators and envelopes.
- **100% Code-Free Constructors**: Constructors only perform attribute assignments (`self._param = param`).
- **Fail-Fast**: Meaningful domain exceptions (`HeaderNotFound`, `RouteNotFound`, `ParamNotFound`) instead of silent `None` checks.
- **Cohesion & Modularity**: Maximum 200 lines per code file; 1 class = 1 file.
- **Zero Reflection Overhead**: Ultra-fast routing and non-blocking I/O.

---

## 📚 Documentation & Guides

- [Routing & Forks Guide](docs/ROUTING.md): Composable routing with `Route`, `Path`, `Get`, `Post`, `Prefix`, `Regex`, `Host`, `HeaderFork`, and `Trap`.
- [HTTP Responses Guide](docs/RESPONSES.md): Composing responses with `Ok`, `Json`, `Text`, `Binary`, `Sse`/`Event`, `Secure`, `Cookie`, `Cached`, and `Gzip`.
- [HTTP Requests Guide](docs/REQUESTS.md): Request inspectors (`BearerToken`, `BasicAuth`, `QueryParams`, `PathParams`), payloads (`Json`, `Multipart`), and test fakes (`Fake`).
- [Developer Console & CLI Guide](docs/CLI.md): Extensible pure OOP CLI architecture, route inspection (`routes`), and server runner (`serve`).
- [Architecture & Requirements](REQUIREMENTS.md): Full architectural specifications, interface details, and compatibility guidelines.

---

## 🧩 Extensions

- [pyaidoc](https://github.com/schillermann/pyaidoc): Zero-annotation, pure OOP HTML documentation and CLI tooling for AI agent tools.
- [pyfakepg](https://github.com/schillermann/pyfakepg): In-memory fake PostgreSQL extension for testing and developing pure OOP database applications.
