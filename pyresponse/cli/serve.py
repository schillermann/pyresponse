"""Serve command starting ASGI server in Pure OOP."""

import importlib
import sys
from typing import Any


class ServeCommand:
    """Starts the ASGI development server with auto-reload."""

    def __init__(
        self,
        app_target: str = "main:app",
        host: str = "0.0.0.0",
        port: int = 8000,
        reload: bool = True,
    ) -> None:
        self._app_target = app_target
        self._host = host
        self._port = port
        self._reload = reload

    def name(self) -> str:
        return "serve"

    def description(self) -> str:
        return f"Start the ASGI server on {self._host}:{self._port} (reload={self._reload})."

    def matches(self, verb: str) -> bool:
        return verb in ("serve", "server", "start")

    def execute(self, args: list[str]) -> int:
        target = args[0] if args else self._app_target
        print(f"🚀 Starting PyResponse server: '{target}' on http://{self._host}:{self._port} ...")
        try:
            uvicorn: Any = importlib.import_module("uvicorn")
            uvicorn.run(target, host=self._host, port=self._port, reload=self._reload)
            return 0
        except ImportError:
            print("❌ Uvicorn is required to run the server. Install via 'pip install uvicorn[standard]'.", file=sys.stderr)
            return 1
