"""CLI entrypoint for AgentSpec Wizard."""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

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


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run gather -> generate -> validate -> write pipeline."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir)
    agentspec_path = output_dir / "agentspec.json"
    claude_md_path = output_dir / "CLAUDE.md"

    if agentspec_path.exists() and not args.force:
        print(f"agentspec.json already exists at {agentspec_path}. Use --force to overwrite.")
        return 1

    try:
        answers = gather_answers()
        spec = generate_spec(answers)
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
    except OSError as exc:
        print(f"Failed to write output files: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
