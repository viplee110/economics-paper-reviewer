# Agent Instructions

This repository defines an English-only portable pre-review skill for economics papers.

Use it when the user asks to review, referee, pre-review, evaluate, or diagnose an English economics paper.

Read `SKILL.md` first, then load the relevant files under `references/`:

- Always load `references/review_pipeline.md`.
- Always load `references/panel_protocol.md`.
- Always load `references/evidence_grounding.md`.
- Load the paper-type lens files that match the classified paper.
- If the user asks to benchmark, validate, or test reviewer quality, also load `references/benchmark_mode.md`.
- If the user asks for scores, calibration, or comparison with human reviewers, also load `references/scorecard.md`.
- Use `references/report_template.md` for the final report shape.

The repository supports Codex, Claude Code, Cursor, and other agent IDEs through thin adapters. The canonical review logic lives in `references/` and must not be duplicated in adapter files.

Keep all outputs in English. In v1, review English economics papers only.
