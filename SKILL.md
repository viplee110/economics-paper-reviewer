---
name: economics-paper-reviewer
description: Review English economics papers as a portable pre-review skill. Use for theory, empirical causal, structural or IO empirical, econometrics or methodology, experimental or behavioral, computational or simulation, and mixed economics papers. Produces evidence-grounded six-role referee reports, fatal/fixable risks, target-fit diagnosis, manuscript architecture diagnosis, and revision priorities.
---

# Economics Paper Reviewer

Use this skill to pre-review an English economics paper. It is an advisory review system, not a final editorial decision or acceptance predictor.

## Core Rule

Run one canonical review protocol across all IDEs:

1. Intake the manuscript, PDF, TeX, or supplied excerpt.
2. Classify paper type: theory, empirical causal, structural, econometrics, experimental, computational, or mixed.
3. Build literature grounding when search tools or user-provided papers are available.
4. Load `references/review_pipeline.md`, `references/panel_protocol.md`, `references/evidence_grounding.md`, and the paper-type lens files needed for the classified paper.
5. Run the six-role economics review panel.
6. Produce the report using `references/report_template.md`.

## Required Six-Role Panel

Always preserve all six roles:

- Referee 1: primary-field specialist.
- Referee 2: closest-literature or adjacent-field specialist.
- Referee 3: method, mechanism, application, or institutional specialist.
- Referee 4: rigor or reproducibility specialist.
- Referee 5: Scientific Judge / Idea Critic.
- Referee 6: Advocate / Best-Case Reader.

## Evidence Discipline

- Search, open, and verify economics literature when tools are available.
- Prefer NBER, SSRN, RePEc/IDEAS, journal pages, working paper pages, OpenAlex, Semantic Scholar, and user-provided PDFs.
- Use arXiv only when relevant to the paper.
- Mark every closest-paper, method-anchor, identification-anchor, absorption-threat, style-anchor, or structure-anchor claim as verified, inferred, or provisional.
- Do not invent citations, datasets, code availability, robustness results, theorem statements, or referee evidence.

## Output Requirements

The review must be in English and include:

- paper type and confidence
- target or venue calibration
- contribution summary
- six-role panel reports
- fatal risks
- fixable risks
- literature and evidence status
- manuscript architecture diagnosis
- recommendation range
- revision priorities

## Boundaries

- Review English economics papers only in v1.
- Do not claim final accept/reject authority.
- Do not use author prestige, institution, gender, nationality, or reputation as evidence.
- If evidence is unavailable, say what is provisional and what must be checked.
