"""CLI entrypoint for AgentSpec Wizard."""
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

from agentspec_wizard.claude_md_writer import write_claude_md
from agentspec_wizard.validator import validate_spec


BlankField = dict[str, Any]


def _build_parser() -> argparse.ArgumentParser:
    """Create and return the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="agentspec-wizard")
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory containing agentspec.json and where CLAUDE.md is written.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Accepted for compatibility. Existing agentspec.json is always updated in place.",
    )
    return parser


def _collect_blank_fields(
    value: Any,
    path: str,
    parent: Any,
    key: Any,
    blanks: list[BlankField],
) -> None:
    """Collect blank fields from a spec tree, skipping _guidance keys."""
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if isinstance(child_key, str) and child_key.startswith("_"):
                continue
            child_path = f"{path}.{child_key}" if path else str(child_key)
            _collect_blank_fields(child_value, child_path, value, child_key, blanks)
        return

    if isinstance(value, list):
        if not value:
            blanks.append({"kind": "list", "path": path, "parent": parent, "key": key})
            return
        for index, item in enumerate(value):
            child_path = f"{path}[{index}]"
            _collect_blank_fields(item, child_path, value, index, blanks)
        return

    if value is None or (isinstance(value, str) and not value.strip()):
        blanks.append({"kind": "string", "path": path, "parent": parent, "key": key})


def _apply_prompt_answers(spec: dict[str, Any]) -> int:
    """Prompt for blank fields found in spec and apply entered values."""
    blanks: list[BlankField] = []
    _collect_blank_fields(spec, "", None, None, blanks)
    if not blanks:
        print("No blank fields found in agentspec.json.")
        return 0

    print(f"Found {len(blanks)} blank fields. Press Enter to skip any field.")
    updates = 0
    for blank in blanks:
        path = blank["path"]
        parent = blank["parent"]
        key = blank["key"]

        if blank["kind"] == "list":
            print(f"{path} (comma-separated values): ", end="", flush=True)
            raw = input().strip()
            if not raw:
                continue
            parent[key] = [item.strip() for item in raw.split(",") if item.strip()]
            updates += 1
            continue

        print(f"{path}: ", end="", flush=True)
        raw = input().strip()
        if not raw:
            continue
        parent[key] = raw
        updates += 1

    return updates


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Load existing spec, prompt for blank fields, and write updates."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir)
    agentspec_path = output_dir / "agentspec.json"
    claude_md_path = output_dir / "CLAUDE.md"

    try:
        if not agentspec_path.exists():
            print(f"agentspec.json not found at {agentspec_path}")
            return 2

        spec_raw = agentspec_path.read_text(encoding="utf-8")
        spec = json.loads(spec_raw)
        if not isinstance(spec, dict):
            print("Failed to read agentspec.json: top-level JSON must be an object.")
            return 2

        updates = _apply_prompt_answers(spec)
        issues = validate_spec(spec)

        claude_md = write_claude_md(spec)
        output_dir.mkdir(parents=True, exist_ok=True)
        agentspec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        claude_md_path.write_text(claude_md, encoding="utf-8")

        print(f"Updated {updates} field(s) in {agentspec_path}")
        print(f"Wrote {claude_md_path}")

        if issues:
            print("Validation issues still remaining:")
            for issue in issues:
                print(f"- {issue}")
            return 1

        return 0
    except (KeyboardInterrupt, EOFError):
        print()
        return 0
    except json.JSONDecodeError as exc:
        print(f"Failed to read agentspec.json: {exc}")
        return 2
    except OSError as exc:
        print(f"Failed to write output files: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
