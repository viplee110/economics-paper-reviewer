# Economics Paper Reviewer

Portable pre-review instructions for English economics papers.

This repository provides a multi-IDE reviewer skill for economics papers. It supports Codex, Claude Code, Cursor, and other agent IDEs through thin adapters, while keeping one canonical review protocol in `references/`.

## Quick Start

Clone or download this repository, then open it from the IDE or agent environment you use for paper review.

```text
Review this economics paper using the economics-paper-reviewer protocol.
```

If your agent can install local skills, use this repository root as the skill folder. The required Codex entry file is `SKILL.md`.

## What It Does

- Reviews English economics papers before submission or revision.
- Classifies the paper as theory, empirical causal, structural, econometrics, experimental, computational, or mixed.
- Runs a six-role economics review panel.
- Grounds review claims in economics literature when tools are available.
- Separates fatal risks from fixable risks.
- Produces target-fit, manuscript architecture, evidence-status, and revision-priority diagnoses.

## What It Does Not Do

- It does not predict acceptance.
- It does not replace human referees or editors.
- It does not certify novelty, theorem correctness, identification validity, or code reproducibility.
- It does not review non-English papers in v1.

## Use With Codex

Install or copy this repository as a Codex skill folder, then ask:

```text
Use the economics-paper-reviewer skill to review this paper.
```

## Use With Claude Code

Clone this repository into or next to your paper project. Claude Code can read `CLAUDE.md`.

Optional slash command:

```text
/review-economics-paper
```

## Use With Cursor Or Other Agent IDEs

Use `AGENTS.md` as the generic entry point, or ask:

```text
Review this economics paper using the repository reviewer instructions.
```

## Repository Layout

```text
SKILL.md
CLAUDE.md
AGENTS.md
references/
eval/
.claude/commands/
.cursor/rules/
```

## Evaluation

The `eval/` folder contains a lightweight benchmark scaffold with toy cases only. It is not a Hugging Face dataset and does not contain copyrighted papers.

## License

Apache-2.0.
