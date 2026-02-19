# AgentSpec

### A structured JSON framework for building software with AI agents — designed for consistency, not chaos.

---

## What This Is

A reusable project template that turns AI coding assistants (Claude, GPT, etc.) from unpredictable autocomplete into a disciplined engineering team.

Instead of dumping your entire codebase into a chat window and hoping for the best, this template gives AI agents:

- **Defined roles** — separate coding, validation, and critique agents with explicit personas and output formats
- **Guardrails** — coding conventions, dependency policies, and project invariants that prevent drift
- **Self-correction loops** — structured validation with severity gating so bad code can't silently advance
- **Session memory** — handoff protocols and decision logs so you never lose context between conversations

It's the difference between "write me some code" and running an actual engineering process.

---

## Who This Is For

- **Solo developers** using AI assistants for real projects (not just one-off scripts)
- **Non-developers directing AI agents** — if you can describe what you want built and what the rules are, AgentSpec lets you manage the process without writing code yourself
- **Small teams** coordinating AI-assisted development across multiple contributors
- **Freelancers and consultants** who want repeatable, professional AI workflows they can use across clients
- **Anyone** who's been burned by AI-generated code that worked in isolation but broke everything else

---

## The Problem This Solves

AI coding assistants are powerful but inconsistent. Without structure, they:

- Rename variables and functions mid-project
- Add dependencies you didn't ask for
- Forget architectural decisions from earlier in the conversation
- Generate code that compiles but violates your project's patterns
- Lose all context when you start a new session

This template eliminates those problems by giving the AI explicit constraints, validation checkpoints, and a persistent project memory.

---

## What's Inside

### Core Structure

| Section | Purpose |
|---|---|
| `project_overview` | What you're building and why (2-3 sentences) |
| `domain_context` | Technical ecosystem — frameworks, patterns, platform quirks |
| `technical_architecture` | Your system's structure — components, relationships, file organization |
| `project_invariants` | **Non-negotiable rules** — the anchor that prevents AI drift |

### Engineering Standards

| Section | Purpose |
|---|---|
| `coding_conventions` | Naming, file size limits, function length limits, style rules |
| `dependency_policy` | What's approved, what needs permission |
| `error_handling_standard` | Required and forbidden error patterns |
| `testing_strategy` | What gets tested, what can skip, coverage targets |

### AI Agent System

| Section | Purpose |
|---|---|
| `agent_prompts` | Persona definitions, context injection order, and structured output formats for coding, validation, and devil's advocate agents |
| `ai_team_guidelines` | Coordination rules — who runs when, iteration limits, escalation paths |
| `ai_principles` | Paired principles and reasoning that shape agent behavior |
| `context_strategy` | What to load, when to load it, and what to never load together |

### Project Management

| Section | Purpose |
|---|---|
| `modules` | Track every component — status, dependencies, risks, acceptance criteria |
| `build_flow` | Your project-specific build sequence |
| `validation_flow` | Compile checks, tests, security checks, quality gates with severity levels |
| `decision_log` | Why decisions were made (invaluable when revisiting a project) |
| `project_health` | At-a-glance status dashboard |
| `handoff_protocol` | Resume any project cleanly after days or weeks away |
| `workflow_diagram` | Mermaid-format visual reference of the agent loop |

---

## Quick Start

### 1. Copy the template

Use `agentspec.json` in your project root as the template file.

### 2. Populate it with AI

You don't need to fill this in manually. Give your AI assistant the empty template along with your project context — notes, docs, conversations, whatever you have — and prompt:

> "Here's my AgentSpec template and my project context. Populate every field in the template using only information from the provided context. Where information is missing, leave the field empty and list what's missing at the end."

The `_guidance` fields inside each section tell the AI exactly what belongs where. Review what it filled in, tweak what you know needs tweaking, and you're ready to build.

**You don't need to be a developer to use AgentSpec.** You need to know what you're building, what matters, and what shouldn't change. The AI handles the rest.

### 3. Fill in anything the AI missed

These five sections are the minimum — if the AI didn't populate them from your context, fill them in yourself:

```
project_overview    → What are you building?
domain_context      → What tech stack?
project_invariants  → What must NEVER change?
coding_conventions  → How do you name things?
modules             → What are the pieces?
```

### 4. Customize agent prompts

Replace the `[ROLE/EXPERTISE]` placeholder in the coding agent's system prompt with a domain-specific persona:

**Trading bot:**
> "You are a senior Python developer specializing in algorithmic trading systems, prediction market mechanics, and API integration with risk management expertise..."

**iOS app:**
> "You are a senior iOS engineer with deep SwiftUI and Combine expertise, focused on clean MVVM architecture and accessibility-first design..."

**Web app:**
> "You are a senior full-stack TypeScript developer specializing in Next.js, serverless architecture, and real-time data systems..."

The persona shapes *how* the agent thinks, not just what it writes.

### 5. Start building

**With Claude Code Agent Teams (recommended):** Follow the setup in the "Using AgentSpec with Claude Code Agent Teams" section below. Three files in your project folder, one launch prompt, and the agents handle the rest.

**Without Claude Code:** Feed the relevant sections to your AI assistant at the start of each session. The `context_strategy` section tells you exactly what to include and when. For returning to a paused project, use the `handoff_protocol.resumption_prompt` — paste it in and the AI will re-orient itself before touching any code.

---

## AgentSpec Wizard (CLI)

This repo now includes a working wizard that generates both `agentspec.json` and `CLAUDE.md` from interactive prompts.

### Run the wizard

From the project root:

```bash
python3 -m agentspec_wizard.cli
```

### Output behavior

- Writes `agentspec.json` and `CLAUDE.md`
- Defaults to current directory
- Refuses to overwrite existing `agentspec.json` unless `--force` is used

### CLI options

```bash
python3 -m agentspec_wizard.cli --output-dir /path/to/project
python3 -m agentspec_wizard.cli --output-dir . --force
```

---

## Using AgentSpec with Claude Code Agent Teams

Agent teams are Claude Code's experimental feature for multi-agent collaboration. Unlike subagents (which work in isolation and report back), agent team members can talk to each other, share a task list, and coordinate automatically.

### Project Setup

```
your-project/
  .claude/
    settings.json          <- enables agent teams
  CLAUDE.md                <- project context (auto-loaded by all teammates)
  agentspec.json           <- this template (source of truth)
```

**`.claude/settings.json`** — just this:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**`CLAUDE.md`** — your project's context file. Every teammate loads this automatically. Include a summary of your project invariants, coding conventions, and terminology, plus the line: "Read agentspec.json for full project governance and agent specifications."

### Launching Your Team

Open Claude Code in your project folder and paste this prompt (customize the module name):

> Read agentspec.json for full project context and agent specifications. Create an agent team with three teammates: a coding agent (use Opus), a validation agent (use Sonnet), and a devil's advocate (use Opus). Use delegation mode — the lead should coordinate only, not implement. Start with [MODULE_NAME] from the modules list. The coding agent builds, the validation agent reviews for correctness and convention compliance, and the devil's advocate critiques design decisions. No module advances to 'stable' with unresolved critical or warning findings. Max 3 correction iterations before escalating to me.

Claude Code creates the team, spawns teammates, builds a task list, and starts coordinating.

### Why You Don't Need Separate `.md` Files Per Agent

Teammates auto-load `CLAUDE.md`, MCP servers, and skills from your project. The team lead creates teammates from your prompt using AgentSpec's agent definitions. No manual markdown files needed — AgentSpec is the single source that drives everything.

### Key Things to Know

- Use **delegation mode** (Shift+Tab) so the lead coordinates instead of coding
- **Shift+Up/Down** cycles between teammates, Enter to view their session
- Teammates **don't inherit conversation history** — context comes from CLAUDE.md only
- **One team per session** — clean up before starting a new one
- **No session resumption** — if you close, teammates are gone. Start fresh.

---

## How the Agent Loop Works

```
Load Context + Invariants
        ↓
Select Module to Build
        ↓
Coding Agent writes code
        ↓
Validation Agent reviews (compile, test, conventions)
        ↓
Devil's Advocate critiques (design, assumptions, risks)
        ↓
    Pass? ──→ Yes → Mark module stable → Next module
      │
      No
      ↓
  Feedback to Coding Agent
      ↓
  Max iterations? ──→ Yes → Escalate to human
      │
      No → Loop back to Coding Agent
```

Every module goes through this loop. No module reaches "stable" with unresolved critical or warning findings.

---

## Key Design Decisions

**Why JSON and not YAML or Markdown?**
JSON is natively parseable by every AI model and programming language. No ambiguity, no indentation issues, no interpretation variance. It's also easy to version control and diff.

**Why separate agent prompts from guidelines?**
Agent prompts define *capabilities and persona* — what the agent is and how it thinks. Guidelines define *coordination rules* — when agents run and how they interact. Mixing them causes duplication and drift.

**Why project invariants?**
This is the single most impactful section in the template. AI models slowly mutate vocabulary, rename patterns, and forget architectural decisions over long sessions. Invariants are the anchor — they get loaded into every prompt and never change unless you explicitly update them.

**Why a devil's advocate agent?**
Code that compiles and passes tests can still be architecturally wrong, make bad assumptions, or create future maintenance nightmares. The devil's advocate catches the category of problems that linters and test suites can't.

---

## Customization Guide

### Fields you MUST fill in for every project
- `project_overview` (all fields)
- `project_invariants.architecture_style`
- `project_invariants.terminology` (at minimum, 5-10 key terms)
- `coding_conventions.naming` (all fields)
- `agent_prompts.coding_agent.system_prompt_template` (replace `[ROLE/EXPERTISE]`)
- `modules` (at least your first 3-5 components)

### Fields you SHOULD fill in
- `project_invariants.non_negotiable_patterns`
- `project_invariants.forbidden_patterns`
- `dependency_policy.approved_dependencies`
- `error_handling_standard.strategy`
- `testing_strategy.approach`
- `validation_flow` (compile_checks, tests, quality_checks)

### Fields that can stay empty until needed
- `decision_log` (populated as you build)
- `build_flow.steps` (populated when planning sprints)
- `skills_reference` (optional skill file links)
- `orchestration` (fill in when you decide manual vs. automated)

---

## Example: Instantiated for a Python Trading Bot

```json
{
  "project_overview": {
    "name": "Polymarket Trading Bot",
    "description": "Autonomous prediction market trading bot with sentiment analysis and risk management",
    "platform": "Linux / macOS CLI",
    "primary_technology": "Python 3.11+",
    "project_type": "trading_bot"
  },
  "project_invariants": {
    "architecture_style": "modular Python package with clear separation between data, strategy, and execution layers",
    "non_negotiable_patterns": [
      "All trades must pass risk validation before execution",
      "No API calls without retry logic and timeout handling",
      "All monetary values use Decimal, never float"
    ],
    "forbidden_patterns": [
      "Hardcoded API keys or secrets",
      "Float arithmetic for financial calculations",
      "Unbounded position sizes",
      "Silent failure on API errors"
    ],
    "terminology": {
      "position": "An active market bet with defined entry price and size",
      "signal": "A scored recommendation from the strategy engine (not a trade)",
      "risk_check": "Validation gate that must pass before any signal becomes a position",
      "dry_run": "Simulation mode that logs would-be trades without executing"
    }
  }
}
```

---

## Version History

| Version | Changes |
|---|---|
| 1.0 | Initial template — basic structure with workflow diagram |
| 2.0 | Added modules, orchestration, handoff protocol, decision log, project health, Mermaid diagram, paired principles/reasoning |
| 2.1 | Added coding conventions, dependency policy, error handling, testing strategy. Consolidated devil's advocate duplication. Added `_guidance` fields for section boundaries |
| 3.0 | Added project invariants for drift prevention. Integrated invariants into context strategy, agent prompts, and validation categories |
| 3.1 | Added module lifecycle metadata, security checks, architecture drift rule, function limits, wired skills_reference and orchestration, added 8th AI principle |
| 3.2 | **Current release.** Replaced vague orchestration section with concrete Claude Code agent teams configuration. Added setup instructions, project structure, launch prompt template, team member definitions with suggested models, agent teams vs subagents guidance, and known limitations. AgentSpec now directly drives Claude Code agent team creation — no separate .md files needed. |

---

## License

MIT License — free to use, modify, and distribute.

---

## Contributing

Found a gap? Have a suggestion? Open an issue or submit a PR. AgentSpec was built through iterative feedback and that process doesn't stop here.
