# agentspec_wizard/questioner.py
"""Questioner module: defines questions and gathers answers from user input."""
from dataclasses import dataclass, field

__all__ = ["Question", "Answers", "gather_answers"]


@dataclass
class Question:
    """A single question to ask the user."""
    field: str
    prompt: str
    required: bool
    default: str


@dataclass
class Answers:
    """All answers gathered from the user.

    Note: non_negotiable_patterns and forbidden_patterns are populated via
    collect_patterns() in gather_answers(), not through QUESTIONS entries.
    """
    project_name: str
    description: str
    platform: str
    primary_technology: str
    project_type: str
    architecture_style: str
    indentation: str
    quotes: str
    non_negotiable_patterns: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)


QUESTIONS: tuple[Question, ...] = (
    Question(
        field="project_name",
        prompt="Project name",
        required=True,
        default="",
    ),
    Question(
        field="description",
        prompt="Brief project description",
        required=True,
        default="",
    ),
    Question(
        field="platform",
        prompt="Target platform (e.g., web, cli, mobile, server)",
        required=True,
        default="",
    ),
    Question(
        field="primary_technology",
        prompt="Primary technology/language",
        required=True,
        default="",
    ),
    Question(
        field="project_type",
        prompt="Project type (e.g., library, application, service)",
        required=True,
        default="",
    ),
    Question(
        field="architecture_style",
        prompt="Architecture style (e.g., modular, layered, microservices)",
        required=False,
        default="modular",
    ),
    Question(
        field="indentation",
        prompt="Indentation style (e.g., 2 spaces, 4 spaces, tabs)",
        required=False,
        default="4 spaces",
    ),
    Question(
        field="quotes",
        prompt="Quote style (single or double)",
        required=False,
        default="double",
    ),
)


def _ask_question(question: Question) -> str:
    """Prompt user for a single question and return the answer."""
    suffix = "" if question.required else f" [{question.default}]"

    while True:
        print(f"{question.prompt}{suffix}: ", end="", flush=True)
        answer = input().strip()

        if answer:
            return answer
        if not question.required:
            return question.default
        print("  This field is required. Please enter a value.")


def _collect_patterns(label: str) -> list[str]:
    """Collect up to 3 patterns from user input.

    Stops when user enters empty input or 3 patterns are collected.
    """
    patterns: list[str] = []
    for n in range(1, 4):
        print(f"{label} pattern {n} (or press Enter to finish): ", end="", flush=True)
        value = input().strip()
        if not value:
            break
        patterns.append(value)
    return patterns


def gather_answers() -> Answers:
    """Run through all questions and return a populated Answers dataclass."""
    try:
        collected: dict[str, str] = {}
        for question in QUESTIONS:
            collected[question.field] = _ask_question(question)

        non_negotiable_patterns = _collect_patterns("Non-negotiable")
        forbidden_patterns = _collect_patterns("Forbidden")

        return Answers(
            **collected,
            non_negotiable_patterns=non_negotiable_patterns,
            forbidden_patterns=forbidden_patterns,
        )
    except (KeyboardInterrupt, EOFError):
        print()
        raise
