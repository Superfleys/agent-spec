"""Build CLAUDE.md content from a spec dict."""
from typing import Any

__all__ = ["write_claude_md"]

_LAUNCH_INSTRUCTION = (
    "Read agentspec.json for full project governance and agent specifications."
)


def _as_text(value: Any) -> str:
    """Return a clean string for markdown output."""
    if not isinstance(value, str):
        return ""
    return value.strip()


def _as_list(value: Any) -> list[str]:
    """Return a list of non-empty strings."""
    if not isinstance(value, list):
        return []
    cleaned: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            cleaned.append(item.strip())
    return cleaned


def _section_list(title: str, values: list[str]) -> list[str]:
    """Return markdown lines for a bulleted section."""
    if not values:
        return []
    lines = [f"## {title}"]
    for value in values:
        lines.append(f"- {value}")
    return lines


def write_claude_md(spec: dict[str, Any]) -> str:
    """Return CLAUDE.md markdown text built from spec content."""
    project = spec.get("project_overview", {})
    invariants = spec.get("project_invariants", {})
    conventions = spec.get("coding_conventions", {})
    naming = conventions.get("naming", {})
    style = conventions.get("style", {})
    terminology = invariants.get("terminology", {})

    name = _as_text(project.get("name"))
    description = _as_text(project.get("description"))
    architecture_style = _as_text(invariants.get("architecture_style"))
    non_negotiable_patterns = _as_list(invariants.get("non_negotiable_patterns"))
    forbidden_patterns = _as_list(invariants.get("forbidden_patterns"))

    lines: list[str] = ["# Project Context", "", _LAUNCH_INSTRUCTION, ""]
    if name:
        lines.extend([f"## {name}", ""])
    if description:
        lines.extend([description, ""])
    if architecture_style:
        lines.extend(["## Architecture Style", architecture_style, ""])

    lines.extend(_section_list("Non-Negotiable Patterns", non_negotiable_patterns))
    if non_negotiable_patterns:
        lines.append("")
    lines.extend(_section_list("Forbidden Patterns", forbidden_patterns))
    if forbidden_patterns:
        lines.append("")

    definition_lines: list[str] = []
    for key, value in terminology.items():
        if key == "_guidance":
            continue
        term = _as_text(key)
        definition = _as_text(value)
        if term and definition:
            definition_lines.extend([term, f": {definition}"])
    if definition_lines:
        lines.extend(["## Terminology", *definition_lines, ""])

    lines.extend(["## Coding Conventions", ""])
    if naming:
        lines.append(
            "Naming: files={files}, functions={functions}, variables={variables}, constants={constants}".format(
                files=_as_text(naming.get("files")),
                functions=_as_text(naming.get("functions")),
                variables=_as_text(naming.get("variables")),
                constants=_as_text(naming.get("constants")),
            )
        )
    if style:
        lines.append(
            "Style: indentation={indentation}, quotes={quotes}".format(
                indentation=_as_text(style.get("indentation")),
                quotes=_as_text(style.get("quotes")),
            )
        )
    return "\n".join(lines).rstrip() + "\n"
