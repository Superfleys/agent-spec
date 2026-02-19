"""AgentSpec Wizard package."""

from typing import Optional, Sequence

__all__ = ["main"]


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Forward to CLI entrypoint without eager module import."""
    from agentspec_wizard.cli import main as cli_main

    return cli_main(argv)
