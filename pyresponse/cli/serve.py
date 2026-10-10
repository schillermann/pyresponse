"""Serve command starting ASGI server in Pure OOP."""

import importlib
from typing import Any
from pyresponse.cli.output import ConsoleOutput, Output
from pyresponse.cli.target import AppTarget


class ServeCommand:
    """Starts the ASGI development server with auto-reload."""

    def __init__(
        self,
        app_target: str = "",
        host: str = "0.0.0.0",
        port: int = 8000,
        reload: bool = True,
        output: Output = ConsoleOutput(),
    ) -> None:
        self._app_target = app_target
        self._host = host
        self._port = port
        self._reload = reload
        self._output = output

    def name(self) -> str:
        return "serve"

    def description(self) -> str:
        return f"Start the ASGI server on {self._host}:{self._port} (reload={self._reload})."

    def matches(self, verb: str) -> bool:
        return verb in ("serve", "server", "start")

    def execute(self, args: list[str]) -> int:
        raw_target = args[0] if args else self._app_target
        target = AppTarget(raw_target).name()
        self._output.print(f"🚀 Starting PyResponse server: '{target}' on http://{self._host}:{self._port} ...")
        try:
            uvicorn: Any = importlib.import_module("uvicorn")
            uvicorn.run(target, host=self._host, port=self._port, reload=self._reload)
            return 0
        except ImportError:
            self._output.error("❌ Uvicorn is required to run the server. Install via 'pip install uvicorn[standard]'.")
            return 1
