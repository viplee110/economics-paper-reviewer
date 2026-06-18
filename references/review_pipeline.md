# Review Pipeline

Use this file as the canonical economics paper pre-review workflow.

## Intake

1. Identify the manuscript source: PDF, TeX, Markdown, DOCX, abstract plus sections, or user-provided excerpt.
2. Build a paper map:
   - title
   - abstract
   - main question
   - paper type
   - target or likely venue class
   - core contribution claim
   - methods
   - data or model status
   - main results
   - appendix and code availability when relevant
3. If the paper is not in English, stop and state that v1 reviews English economics papers only.

## Paper-Type Routing

Classify the paper before reviewing. Use one or more lenses:

- theory: use `theory_review.md`
- empirical causal: use `empirical_review.md`
- structural or IO empirical: use `structural_review.md`
- econometrics or methodology: use `econometrics_review.md`
- experimental or behavioral: use `experimental_review.md`
- computational or simulation: use `computational_review.md`
- mixed: load every relevant lens and state the dominant review risk

## Grounding

Use `evidence_grounding.md` before making serious novelty, contribution, target-fit, or methods claims.

If search tools are unavailable, state which judgments are provisional.

## Review

Run the six-role panel in `panel_protocol.md`.

The panel should distinguish:

- weak idea
- weak execution
- weak identification or proof
- weak literature positioning
- weak manuscript architecture
- weak exposition
- missing evidence

## Output

Use `report_template.md`.

Do not collapse the review to a single score. If a score is requested, provide it only after the written diagnosis and explain its uncertainty.
