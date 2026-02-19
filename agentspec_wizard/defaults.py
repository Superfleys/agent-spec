# agentspec_wizard/defaults.py
"""Static default sections for the agentspec dict. Pure data, no I/O."""
from typing import Any

__all__ = ["build_boilerplate_defaults", "build_orchestration_defaults"]


def build_boilerplate_defaults() -> dict[str, Any]:
    """Return all boilerplate sections keyed by top-level name."""
    return {
        "domain_context": {
            "_guidance": "Technical environment only — frameworks, patterns, and gotchas specific to the domain.",
            "frameworks": [],
            "high_level_design_patterns": [],
            "technical_notes": [],
        },
        "dependency_policy": {
            "approved_dependencies": [],
            "approval_required_for_new": True,
            "prefer_built_in_over_third_party": True,
            "notes": "",
        },
        "error_handling_standard": {
            "strategy": "",
            "required_patterns": [],
            "forbidden_patterns": [],
        },
        "testing_strategy": {
            "approach": "",
            "minimum_coverage_target": "",
            "test_naming_convention": "",
            "what_must_be_tested": [],
            "what_can_skip_tests": [],
        },
        "skills_reference": {
            "_guidance": "Links to skill files, style guides, or reference docs that agents should consult for domain-specific patterns.",
            "files": [],
        },
        "ai_principles": {"principles": []},
        "decision_log": [],
        "project_health": {
            "total_modules": 1,
            "stable": 0,
            "in_progress": 0,
            "draft": 1,
            "blocked": 0,
            "current_iteration_focus": "",
            "last_escalation": "",
        },
        "handoff_protocol": {
            "resumption_prompt": "",
            "context_minimum_for_resumption": [],
            "stale_threshold_days": 7,
            "stale_action": "",
        },
    }


def _agent_team_section() -> dict[str, Any]:
    """Return claude_code_agent_team with full schema structure."""
    return {
        "_guidance": "Configuration for Claude Code's experimental agent teams feature.",
        "setup": {
            "required_file": ".claude/settings.json",
            "required_content": {"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}},
            "project_structure": [],
        },
        "claude_md_should_contain": [],
        "team_structure": {"team_lead": "", "teammates": []},
        "launch_prompt_template": "",
        "important_notes": [],
    }


def build_orchestration_defaults() -> dict[str, Any]:
    """Return all orchestration-related sections."""
    return {
        "orchestration": {
            "_guidance": "How agents coordinate work.",
            "method": "claude_code_agent_team",
            "method_options": [
                "claude_code_agent_team: Claude Code spawns teammates that coordinate via shared task list and direct messaging.",
                "claude_code_subagents: Single session kicks off isolated background workers.",
                "manual_sequential: You paste context into each AI conversation manually.",
                "human_in_loop: Human reviews and approves between each agent step.",
            ],
            "claude_code_agent_team": _agent_team_section(),
        },
        "context_strategy": {
            "max_lines_per_prompt": 300,
            "priority_order": [],
            "always_include": [],
            "include_when_relevant": [],
            "never_include_together": [],
        },
        "agent_prompts": {
            "coding_agent": "",
            "validation_agent": "",
            "devils_advocate_agent": "",
        },
        "ai_team_guidelines": {
            "_guidance": "Behavioral rules for AI agents. Defines coordination, not agent capabilities.",
            "when_to_use_multiple_agents": "",
            "when_to_use_agent_teams_vs_subagents": "",
            "rules_for_coordination": [],
            "max_correction_iterations": 3,
            "fallback_on_max": "",
        },
        "build_flow": {
            "_guidance": "Project-specific execution sequence.",
            "steps": [],
        },
        "validation_flow": {
            "compile_checks": [],
            "tests": [],
            "quality_checks": [],
            "security_checks": [],
            "severity_levels": {},
            "gate_policy": "",
        },
    }
