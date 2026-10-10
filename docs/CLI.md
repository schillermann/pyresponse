# 🛠️ PyResponse Developer Console & CLI Guide

> **Pure OOP Command-Line Interface**  
> Elegant Objects (Yegor Bugayenko), Zero-Annotation, Composable Console Commands.

---

## 1. Overview

`pyresponse` provides an autonomous, extensible CLI architecture modeled after Yegor Bugayenko's *Takes* and *Elegant Objects* principles:
- **No argparse spaghetti**: Commands are autonomous domain objects conforming to the `CliCommand` protocol.
- **Polymorphic Routing**: `ForkCli` evaluates commands without procedural `if/elif` branching.
- **Fail-Fast**: Unknown commands return exit code `1` via `UnknownCommand`.
- **Zero Framework Coupling**: Applications compose commands explicitly at the composition root (`cli.py`).

---

## 2. Built-in Commands

When running `pyresponse` or the `pyr` alias directly via CLI or `CliApp`:

| Command | Description | Example |
| :--- | :--- | :--- |
| **`serve`** | Starts the ASGI development server with auto-reload. | `pyr serve main:app` |
| **`routes`** | Inspects and displays all registered HTTP routes in an ANSI table. | `pyr routes` |
| **`help`** | Shows available commands with usage descriptions. | `pyr help` |

### Terminal Route Inspection (`pyr routes`)
`RoutesCommand` inspects a `Fork` tree and prints a clean overview:
```text
METHOD    PATH                                    HANDLER
──────────────────────────────────────────────────────────────────────────
POST      /api/auth/login                         Login
GET       /api/auth/me                            CurrentUser
GET       /api/chat/stream                        Stream
...
Total: 56 routes
```

---

## 3. Creating Custom Commands

To create a new command, implement the `CliCommand` protocol:

```python
from pyresponse.cli import Arguments, CliCommand, ExitCode, Success


class DatabaseMigrateCommand:
    """Runs pending database migrations."""

    def __init__(self, migration_service) -> None:
        self._migration_service = migration_service

    def name(self) -> str:
        return "db:migrate"

    def description(self) -> str:
        return "Apply all pending database schema migrations."

    def matches(self, verb: str) -> bool:
        return verb in ("db:migrate", "migrate")

    def execute(self, args: Arguments) -> ExitCode:
        self._migration_service.apply()
        print("✅ Migrations applied successfully.")
        return Success()
```

---

## 4. Application Composition Root (`cli.py`)

In your project, compose your application's CLI explicitly:

```python
#!/usr/bin/env python3
from pyresponse.cli import (
    Arguments,
    ExitCode,
    ForkCli,
    HelpCommand,
    RoutesCommand,
    ServeCommand,
    Success,
    SysArguments,
)
from my_app.routes import AppRoutes
from my_app.custom_command import DatabaseMigrateCommand

def main(args: Arguments = SysArguments()) -> ExitCode:
    commands = (
        DatabaseMigrateCommand(),
        RoutesCommand(lambda: AppRoutes().fork()),
        ServeCommand("my_app.main:app"),
    )
    help_cmd = HelpCommand(commands)
    return ForkCli((*commands, help_cmd), fallback=help_cmd).execute(args)

if __name__ == "__main__":
    main().terminate()
```

---

## 5. Plug-in Discovery via Entry Points

Third-party packages (such as `pyaidoc`) can contribute commands to `pyresponse` without hard-coded dependencies by declaring `entry_points` in their `pyproject.toml`:

```toml
[project.entry-points."pyresponse.commands"]
ai_tools = "pyaidoc.cli:AiToolsCommand"
```

The `DiscoveredCommands` object in `pyresponse.cli` automatically loads these commands when `CliApp` runs.
