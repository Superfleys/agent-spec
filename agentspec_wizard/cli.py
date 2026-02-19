"""CLI entrypoint for AgentSpec Wizard."""
import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

from agentspec_wizard.claude_md_writer import write_claude_md
from agentspec_wizard.generator import generate_spec
from agentspec_wizard.questioner import gather_answers
from agentspec_wizard.validator import validate_spec


def _build_parser() -> argparse.ArgumentParser:
    """Create and return the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="agentspec-wizard")
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write agentspec.json and CLAUDE.md.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without prompting.",
    )
    return parser


def _ensure_dict(parent: dict[str, Any], key: str) -> dict[str, Any]:
    """Return parent[key] as dict, creating an empty dict if needed."""
    value = parent.get(key)
    if isinstance(value, dict):
        return value
    parent[key] = {}
    return parent[key]


def _apply_answers_to_spec(existing_spec: dict[str, Any], generated_spec: dict[str, Any]) -> dict[str, Any]:
    """Update form-like fields in an existing spec while preserving everything else."""
    spec = copy.deepcopy(existing_spec)
    spec["last_updated"] = generated_spec.get("last_updated", "")

    project_overview = _ensure_dict(spec, "project_overview")
    generated_overview = generated_spec.get("project_overview", {})
    for key in ("name", "description", "platform", "primary_technology", "project_type"):
        project_overview[key] = generated_overview.get(key, "")

    project_invariants = _ensure_dict(spec, "project_invariants")
    generated_invariants = generated_spec.get("project_invariants", {})
    project_invariants["architecture_style"] = generated_invariants.get("architecture_style", "")
    project_invariants["non_negotiable_patterns"] = generated_invariants.get("non_negotiable_patterns", [])
    project_invariants["forbidden_patterns"] = generated_invariants.get("forbidden_patterns", [])

    coding_conventions = _ensure_dict(spec, "coding_conventions")
    style = _ensure_dict(coding_conventions, "style")
    generated_style = generated_spec.get("coding_conventions", {}).get("style", {})
    style["indentation"] = generated_style.get("indentation", "")
    style["quotes"] = generated_style.get("quotes", "")
    return spec


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run gather -> generate -> validate -> write pipeline."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir)
    agentspec_path = output_dir / "agentspec.json"
    claude_md_path = output_dir / "CLAUDE.md"

    try:
        answers = gather_answers()
        generated_spec = generate_spec(answers)

        if agentspec_path.exists():
            existing_spec = json.loads(agentspec_path.read_text(encoding="utf-8"))
            if not isinstance(existing_spec, dict):
                print("Failed to read agentspec.json: top-level JSON must be an object.")
                return 2
            spec = _apply_answers_to_spec(existing_spec, generated_spec)
        else:
            spec = generated_spec

        issues = validate_spec(spec)
        if issues:
            print("Validation issues:")
            for issue in issues:
                print(f"- {issue}")
            return 1

        claude_md = write_claude_md(spec)
        output_dir.mkdir(parents=True, exist_ok=True)
        agentspec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        claude_md_path.write_text(claude_md, encoding="utf-8")
        print(f"Wrote {agentspec_path}")
        print(f"Wrote {claude_md_path}")
        return 0
    except (KeyboardInterrupt, EOFError):
        return 0
    except json.JSONDecodeError as exc:
        print(f"Failed to read agentspec.json: {exc}")
        return 2
    except OSError as exc:
        print(f"Failed to write output files: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
