# Economics Paper Reviewer

Portable pre-review instructions for English economics papers.

This repository provides a multi-IDE reviewer skill for economics papers. It supports Codex, Claude Code, Cursor, and other agent IDEs through thin adapters, while keeping one canonical review protocol in `references/`.

## Start Here

You only need three things:

1. This repository.
2. Your English economics paper, draft, PDF, TeX folder, or excerpt.
3. An AI coding or agent IDE such as Codex, Claude Code, Cursor, or another tool that can read repository instructions.

Then say:

```text
Review this economics paper using the economics-paper-reviewer protocol.
```

The reviewer will classify the paper, load the right economics lens, run a six-role panel, and tell you which claims are verified, provisional, fatal, or fixable.

If you ask for scores or benchmarking, it also produces a stable multidimensional scorecard that can be calibrated against human reviewer ratings.

## Easiest Install Options

### Option A: Download ZIP

Use this if you do not like Git.

1. Click `Code` on GitHub.
2. Click `Download ZIP`.
3. Unzip the folder.
4. Put the folder next to your paper project or inside your agent skills folder.
5. Open your paper project in your AI IDE.
6. Ask the agent to review your paper using this repository's instructions.

### Option B: Git Clone

Use this if you are comfortable with Git:

```powershell
git clone https://github.com/viplee110/economics-paper-reviewer.git
```

Then open either your paper project or this reviewer folder in your AI IDE.

## What To Give The Reviewer

Best:

- the full paper PDF
- the TeX source folder
- appendix, tables, figures, and code notes when relevant
- target journal or venue if you have one

Still useful:

- title, abstract, introduction, model or empirical design section
- a working-paper excerpt
- a referee response draft

If evidence is missing, the reviewer must mark the corresponding judgment as provisional.

## What It Does

- Reviews English economics papers before submission or revision.
- Classifies the paper as theory, empirical causal, structural, econometrics, experimental, computational, survey or literature review, or mixed.
- Runs a six-role economics review panel.
- Grounds review claims in economics literature when tools are available.
- Separates fatal risks from fixable risks.
- Runs a false-fatal audit so severe criticisms do not mechanically reject papers with real economic value.
- Produces target-fit, manuscript architecture, evidence-status, and revision-priority diagnoses.
- Produces a multidimensional reviewer scorecard for benchmark and calibration tasks.

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

Simple local install paths:

```text
Windows: C:\Users\<you>\.codex\skills\economics-paper-reviewer
macOS/Linux: ~/.codex/skills/economics-paper-reviewer
```

If you do not install it as a skill, you can still clone or download this repository and ask Codex to use the `SKILL.md` file in this folder.

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

If the IDE asks which instruction file to use, choose `AGENTS.md`.

## Plain-English Workflow

The reviewer follows this order:

1. Identify the paper type.
2. Check the contribution claim.
3. Check the closest literature and evidence status.
4. List must-not-miss risks.
5. Run six separate referee roles.
6. Separate fatal risks from fixable risks.
7. Audit false-fatal criticisms and best-case defenses.
8. Diagnose paper structure and target fit.
9. Add a scorecard if scores or benchmarks are requested.
10. Give prioritized revision steps.

The output is a pre-review report, not a final editorial decision.

## Repository Layout

```text
SKILL.md
CLAUDE.md
AGENTS.md
EVALUATION.md
references/
eval/
.claude/commands/
.cursor/rules/
```

## Evaluation

The `eval/` folder contains a lightweight benchmark scaffold with toy cases only. It is not a Hugging Face dataset and does not contain copyrighted papers. See `EVALUATION.md` for the evaluation strategy and the boundary between pipeline tests and economics-validity tests.

For validation or benchmark tasks, ask:

```text
Benchmark this reviewer on this economics paper.
```

For Ng-style human-correlation tests, use the scorecard dimensions as calibration features. Keep raw skill performance and calibrated test-set performance separate.

## License

MIT.
