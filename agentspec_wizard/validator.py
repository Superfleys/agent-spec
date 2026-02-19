"""
Validator module for AgentSpec Wizard.

Pure function that validates a spec dict and returns a list of issues.
No input(), no print(), no file I/O, never raises exceptions.
"""

from typing import Any, List, Tuple


REQUIRED_FIELDS: Tuple[str, ...] = (
    "version",
    "project_overview.name",
    "project_overview.description",
    "project_invariants.architecture_style",
    "modules",
    "coding_conventions.naming.files",
)


def _get_nested(spec: dict, path: str) -> Any:
    """
    Safely retrieve a nested value from spec using dot notation.
    Returns None if any key in the path is missing.
    """
    keys = path.split(".")
    current = spec
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
        if current is None:
            return None
    return current


def _is_empty(value: Any) -> bool:
    """
    Check if a value is considered empty for validation purposes.
    Empty means: None, empty string, whitespace-only string, or empty list.
    """
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


def _check_field(spec: dict, path: str, issues: List[str]) -> None:
    """
    Check a single field path and append an issue if missing or empty.
    Mutates the issues list in place.
    """
    value = _get_nested(spec, path)
    if _is_empty(value):
        issues.append(f"{path} is required but empty")


def validate_spec(spec: dict) -> List[str]:
    """
    Validate a spec dict and return a list of all issues found.

    Returns an empty list if the spec is valid.
    Collects ALL issues — does not short-circuit on first failure.
    """
    issues: List[str] = []
    for path in REQUIRED_FIELDS:
        _check_field(spec, path, issues)
    return issues
