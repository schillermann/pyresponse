"""Application target loader for pyresponse CLI in Pure OOP."""

import importlib
import os
import sys
from typing import Any


class AppTarget:
    """Encapsulates target loading and route extraction."""

    def __init__(self, target: str = "") -> None:
        self._target = target

    def name(self) -> str:
        if self._target:
            return self._target
        return os.getenv("PYRESPONSE_APP", "main:app")

    def load(self) -> Any:
        full_name = self.name()
        if ":" in full_name:
            mod_name, attr_name = full_name.split(":", 1)
        else:
            mod_name, attr_name = full_name, "app"

        cwd = os.getcwd()
        parent = os.path.dirname(cwd)
        for directory in (cwd, os.path.join(cwd, "backend"), parent, os.path.join(parent, "backend")):
            if os.path.isdir(directory) and directory not in sys.path:
                sys.path.insert(0, directory)

        module = importlib.import_module(mod_name)
        return getattr(module, attr_name)

    def routes(self) -> Any:
        app_obj = self.load()
        if hasattr(app_obj, "routes") and callable(app_obj.routes):
            return app_obj.routes()
        portal_fn: Any = getattr(app_obj, "portal", None)
        if callable(portal_fn):
            portal = portal_fn()
            portal_routes_fn: Any = getattr(portal, "routes", None)
            if callable(portal_routes_fn):
                return portal_routes_fn()
        inner = getattr(app_obj, "_origin", None) or getattr(app_obj, "_app", None)
        if inner is not None:
            return inner
        return app_obj
