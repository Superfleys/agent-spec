# agentspec_wizard/generator.py
"""Generator module: pure function that builds spec dict from Answers."""
from datetime import date
from typing import Any

from agentspec_wizard.defaults import (
    build_boilerplate_defaults,
    build_orchestration_defaults,
)
from agentspec_wizard.questioner import Answers

__all__ = ["generate_spec"]

_INSTRUCTION = (
    "When you read this file, create an agent team using the"
    " orchestration.claude_code_agent_team section. Use delegation"
    " mode (Shift+Tab) — the lead should coordinate only, not"
    " implement. Start with the first module in the modules list"
    " unless told otherwise."
)


def _build_project_overview(answers: Answers) -> dict[str, Any]:
    """Build the project_overview section."""
    return {
        "_guidance": "High-level what and why. Keep to 2-3 sentences max. No technical details here.",
        "name": answers.project_name,
        "description": answers.description,
        "platform": answers.platform,
        "primary_technology": answers.primary_technology,
        "project_type": answers.project_type,
    }


def _build_technical_architecture(answers: Answers) -> dict[str, Any]:
    """Build the technical_architecture section."""
    return {
        "_guidance": "How YOUR system is structured. Components, relationships, and file organization.",
        "architecture_summary": answers.architecture_style,
        "major_components": [],
        "file_structure_overview": [],
    }


def _build_project_invariants(answers: Answers) -> dict[str, Any]:
    """Build the project_invariants section."""
    return {
        "_guidance": "Non-negotiable rules the AI must never deviate from.",
        "architecture_style": answers.architecture_style,
        "architecture_drift_rule": "",
        "non_negotiable_patterns": answers.non_negotiable_patterns,
        "forbidden_patterns": answers.forbidden_patterns,
        "terminology": {
            "_guidance": "Canonical terms — AI must never rename or drift on these.",
        },
    }


def _build_coding_conventions(answers: Answers) -> dict[str, Any]:
    """Build the coding_conventions section."""
    return {
        "naming": {
            "files": "snake_case",
            "functions": "snake_case, verb-first",
            "variables": "snake_case",
            "constants": "UPPER_SNAKE_CASE",
            "examples": [],
        },
        "file_rules": {
            "max_lines_per_file": 150,
            "one_responsibility_per_file": True,
            "folder_structure_notes": "",
        },
        "function_rules": {
            "max_function_length": "30 lines",
            "max_parameters_per_function": "4",
        },
        "style": {
            "indentation": answers.indentation,
            "quotes": answers.quotes,
            "trailing_commas": "",
            "additional_rules": [],
        },
    }


def _build_module_placeholder() -> dict[str, Any]:
    """Build a single placeholder module entry."""
    return {
        "name": "placeholder",
        "file_path": "",
        "status": "draft",
        "depends_on": [],
        "blocked_by": [],
        "estimated_complexity": "",
        "known_risks": [],
        "acceptance_criteria": [],
        "last_modified": "",
        "iteration_count": 0,
        "test_status": "untested",
        "owner_agent": "",
        "notes": "",
    }


def _build_workflow_diagram() -> dict[str, Any]:
    """Build the workflow_diagram section."""
    return {
        "_guidance": "Human-readable visualization only. Not operational logic.",
        "format": "mermaid",
        "diagram": "",
        "description": "",
    }


def generate_spec(answers: Answers, today: str = "") -> dict[str, Any]:
    """Generate a complete agentspec dict from user answers."""
    if not today:
        today = date.today().isoformat()
    bp = build_boilerplate_defaults()
    orch = build_orchestration_defaults()
    return {
        "_instruction": _INSTRUCTION,
        "version": "3.3",
        "last_updated": today,
        "project_overview": _build_project_overview(answers),
        "domain_context": bp["domain_context"],
        "technical_architecture": _build_technical_architecture(answers),
        "project_invariants": _build_project_invariants(answers),
        "coding_conventions": _build_coding_conventions(answers),
        "dependency_policy": bp["dependency_policy"],
        "error_handling_standard": bp["error_handling_standard"],
        "testing_strategy": bp["testing_strategy"],
        "modules": [_build_module_placeholder()],
        "skills_reference": bp["skills_reference"],
        "orchestration": orch["orchestration"],
        "context_strategy": orch["context_strategy"],
        "agent_prompts": orch["agent_prompts"],
        "ai_team_guidelines": orch["ai_team_guidelines"],
        "build_flow": orch["build_flow"],
        "validation_flow": orch["validation_flow"],
        "ai_principles": bp["ai_principles"],
        "decision_log": bp["decision_log"],
        "project_health": bp["project_health"],
        "handoff_protocol": bp["handoff_protocol"],
        "workflow_diagram": _build_workflow_diagram(),
    }
