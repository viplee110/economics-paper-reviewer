# Evaluation Strategy

This repository is a review protocol and skill scaffold, not a trained model. Evaluation should therefore separate pipeline robustness from economics review validity.

## Core Principle

Computer science peer-review datasets can test pipeline robustness, but they cannot establish economics review validity.

Do not report performance on CS review datasets as evidence that this skill has professional economics referee validity. A CS benchmark may show that the system can parse papers, follow instructions, preserve output format, and avoid hallucinated evidence under long-document pressure. It cannot show that the reviewer understands identification, equilibrium logic, structural estimation, economic mechanisms, econometric assumptions, or economics field taste.

## Evaluation Layers

1. Static skill checks.
   Validate that `SKILL.md`, `CLAUDE.md`, and `AGENTS.md` point to the same canonical protocol, that all six referee roles are present, and that every lens-based paper type has a lens in `references/`. Mixed papers should load every relevant lens rather than a separate mixed-only lens.

2. Pipeline robustness tests.
   General peer-review datasets, including CS datasets, may be used to test parsing, long-document stability, formatting discipline, citation-label discipline, and resistance to generic output. These tests are engineering checks only.

3. Economics routing tests.
   Use legally clean toy cases and open-access economics cases to test whether the reviewer selects the correct lens: theory, empirical causal, structural, econometrics, experimental, computational, survey or literature review, or mixed.

4. Economics validity proxy tests.
   Use economics-specific evidence when legally available:
   - early working paper versus final published version comparisons
   - public peer-review files for economics-related papers
   - author response or rebuttal files when public
   - expert spot checks by economists
   - known published papers as calibration controls

5. Human usefulness tests.
   Ask economists whether the review identifies real fatal risks, fixable risks, missing literature, manuscript-architecture problems, and revision priorities.

## Suggested Metrics

- Paper-type routing accuracy.
- Raw reviewer-score correlation with human ratings.
- Calibrated score correlation with human ratings on a held-out test split.
- Acceptance or revise-and-resubmit AUC when valid human outcome labels exist.
- Must-not-miss risk recall.
- Hallucination rate for citations, data, proofs, methods, and results.
- Provisional-label discipline when evidence is missing.
- False-fatal rate on known published control papers.
- Best-case reconstruction quality.
- Must-not-miss risk recall.
- Appendix-inspection discipline before fatal claims.
- Evidence-that-would-change-the-decision clarity.
- Actionability of revision priorities.
- Expert usefulness rating.

## Ng-Style Calibration Tests

For comparison with agentic reviewer systems that train a simple calibration model, use a split-sample design:

1. Use full paper text, not abstract-only or excerpt-only inputs.
2. Produce blind reviews and scorecards for every paper before opening human labels.
3. Validate the blind review file with `eval/scripts/validate_scorecards.py`.
4. Split the benchmark into a training set and a held-out test set before fitting any calibrator.
5. Train a simple model, such as linear regression, using the scorecard dimensions as features and human mean reviewer ratings as the target.
6. Report raw skill performance and calibrated test-set performance separately.
7. Do not tune prompts, score definitions, or model weights on the held-out test set.

The committed scorecard dimensions live in `references/scorecard.md` so benchmark features stay stable across IDEs.

See `eval/benchmark_protocol.md` for the full benchmark protocol.

## What Not To Claim

Do not claim:

- accept/reject prediction accuracy
- top-journal referee equivalence
- proof correctness certification
- identification validity certification
- novelty certification
- economics-wide validity from CS-only benchmarks

## Data Policy

- Use open-access papers, user-provided papers, or metadata-only cases unless permission is clear.
- Do not commit copyrighted PDFs.
- Store local downloads and generated external-pilot outputs in ignored folders such as `review_outputs/`.
- Commit only toy cases, legally clean metadata, and evaluation instructions.

## Current Repository Scope

The committed `eval/` folder is intentionally lightweight. It is a scaffold for checking routing and review discipline, not a public benchmark dataset. A larger benchmark can be split into a separate repository or released on Hugging Face later if the cases are legally clean and the evaluation protocol is stable.
