"""Tools package for GenericAgent.

This package provides built-in tools that the agent can use during execution.
Each tool module should define a `schema` dict (OpenAI function schema) and
a callable `handler` function that implements the tool logic.
"""

from pathlib import Path
import importlib
import json

_TOOLS_DIR = Path(__file__).parent


def discover_tools() -> list[dict]:
    """Discover and return all tool schemas from this package.

    Scans the tools directory for modules that expose a `schema` attribute
    and collects them into a list suitable for passing to the OpenAI API.

    Returns:
        List of function schema dicts.
    """
    schemas = []
    for path in sorted(_TOOLS_DIR.glob("*.py")):
        if path.stem.startswith("_"):
            continue
        module = importlib.import_module(f"tools.{path.stem}")
        if hasattr(module, "schema"):
            schemas.append(module.schema)
    return schemas


def get_handler(tool_name: str):
    """Return the handler callable for a named tool.

    Args:
        tool_name: The name of the tool as declared in its schema.

    Returns:
        The handler callable, or None if not found.
    """
    for path in _TOOLS_DIR.glob("*.py"):
        if path.stem.startswith("_"):
            continue
        module = importlib.import_module(f"tools.{path.stem}")
        if hasattr(module, "schema") and module.schema.get("name") == tool_name:
            return getattr(module, "handler", None)
    return None
