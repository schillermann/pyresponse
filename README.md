# pyresponse

A simple web framework in Python that respects OOP.

Inspired by pure OOP, Alan Kay with [Smalltalk](https://en.wikipedia.org/wiki/Smalltalk), and Yegor Bugayenko's [Cactoos](https://github.com/yegor256/cactoos), [Takes](https://github.com/yegor256/takes), and [JPages](https://github.com/yegor256/jpages).

I’ve also created the web framework in other languages that you can check out.
- [Java](https://github.com/schillermann/jresponses)
- [JavaScript](https://github.com/schillermann/jsresponses)
- [PhpResponse](https://github.com/schillermann/phpresponse)

---

## 🎯 Motivation & Philosophy

Most modern Python web frameworks (FastAPI, Flask, Django) heavily rely on:
- Global state and singletons (`app = FastAPI()`, global dependency containers)
- Prozedural routing decorators (`@app.get(...)`, `@app.post(...)`)
- Anemic data structures (DTOs with getters/setters or raw dictionaries)
- Reflection-based magic dependency injection

## Core Principles
- **Strictly OOP**: No getters, no setters, no nulls.
- **Composition over Inheritance**: Functionality is built using decorators.
- **Immutability**: Responses are defined through nested objects.

---

## 📚 Documentation & Specification

See [REQUIREMENTS.md](REQUIREMENTS.md) for full architectural specifications, interface details, and compatibility guidelines.
