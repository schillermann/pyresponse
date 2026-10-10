"""Routes inspection and table formatting for pyresponse CLI in Pure OOP."""

from typing import Any, Sequence
from pyresponse.cli.target import AppTarget


class RouteEntry:
    """Encapsulates a single inspected HTTP route."""

    def __init__(self, method: str, path: str, handler: str) -> None:
        self._method = method
        self._path = path
        self._handler = handler

    def method(self) -> str:
        return self._method

    def path(self) -> str:
        return self._path

    def handler(self) -> str:
        return self._handler


class RoutesInspector:
    """Traverses a Fork tree to extract route definitions."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def entries(self, prefix: str = "") -> list[RouteEntry]:
        return self.traverse(self._origin, prefix)

    def traverse(self, node: Any, path: str) -> list[RouteEntry]:
        results: list[RouteEntry] = []
        if node is None:
            return results

        if isinstance(node, (list, tuple)):
            for child in node:
                results.extend(self.traverse(child, path))
            return results

        node_prefix = getattr(node, "_prefix", None)
        if node_prefix is not None:
            combined = f"{path.rstrip('/')}/{str(node_prefix).lstrip('/')}"
            origin = getattr(node, "_origin", None)
            return self.traverse(origin, combined)

        pattern = getattr(node, "_pattern", None)
        if pattern is not None:
            combined = f"{path.rstrip('/')}/{str(pattern).lstrip('/')}"
            origin = getattr(node, "_origin", None)
            return self.traverse(origin, combined)

        method = getattr(node, "METHOD", None)
        if method is not None:
            m_or_e = getattr(node, "_method_or_endpoint", None)
            ep = getattr(node, "_endpoint", None)
            if isinstance(m_or_e, str):
                route_path = f"{path.rstrip('/')}/{m_or_e.lstrip('/')}"
                target = ep or node
            else:
                route_path = path if path else "/"
                target = ep or m_or_e or node
            handler_name = target.__class__.__name__ if target else node.__class__.__name__
            return [RouteEntry(method, route_path, handler_name)]

        branches = getattr(node, "_branches", None)
        if branches is not None:
            for branch in branches:
                results.extend(self.traverse(branch, path))
            return results

        endpoint = getattr(node, "_endpoint", None)
        if endpoint is not None and endpoint is not node:
            return self.traverse(endpoint, path)

        origin = getattr(node, "_origin", None)
        if origin is not None and origin is not node:
            return self.traverse(origin, path)

        return results


class RoutesTable:
    """Renders route entries as an ANSI formatted terminal table."""

    def __init__(self, entries: Sequence[RouteEntry]) -> None:
        self._entries = entries

    def text(self) -> str:
        if not self._entries:
            return "No routes registered.\n"

        max_method = max([len(e.method()) for e in self._entries], default=6)
        max_path = max([len(e.path()) for e in self._entries], default=20)

        lines = [
            f"\n{'METHOD'.ljust(max_method + 2)}{'PATH'.ljust(max_path + 4)}HANDLER",
            "─" * (max_method + max_path + 30),
        ]
        for e in self._entries:
            lines.append(f"{e.method().ljust(max_method + 2)}{e.path().ljust(max_path + 4)}{e.handler()}")
        lines.append(f"\nTotal: {len(self._entries)} routes\n")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.text()


class RoutesCommand:
    """CLI command displaying registered application routes."""

    def __init__(self, routes_provider: Any = None) -> None:
        self._routes_provider = routes_provider

    def name(self) -> str:
        return "routes"

    def description(self) -> str:
        return "Inspect and list all registered HTTP routes."

    def matches(self, verb: str) -> bool:
        return verb in ("routes", "route:list")

    def execute(self, args: list[str]) -> int:
        target = args[0] if args else ""
        if self._routes_provider is not None:
            root = self._routes_provider() if callable(self._routes_provider) else self._routes_provider
        else:
            root = AppTarget(target).routes()
        entries = RoutesInspector(root).entries()
        print(RoutesTable(entries))
        return 0

