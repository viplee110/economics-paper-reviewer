# Reviewer Scorecard

Use this scorecard whenever the review output needs stable numeric features for benchmarking, calibration, or comparison with human reviewer ratings.

## Core Rule

The scorecard is a calibration layer, not a substitute for the written review. Always write the must-not-miss risks, six-role panel, fatal/fixable risks, and false-fatal audit before interpreting the numbers.

## Scale

Use a 1-10 scale for every dimension.

- 1-2: severe weakness
- 3-4: weak
- 5: mixed or uncertain
- 6: promising but incomplete
- 7: strong
- 8: very strong
- 9-10: exceptional

Mark a dimension `provisional` when the required evidence is missing.

## Dimensions

Report these dimensions in this order:

1. `originality`
   - Does the paper offer a nontrivial new question, mechanism, method, dataset, fact, theorem, or interpretation?
2. `importance`
   - Would the contribution matter for the target field, journal, policy question, model class, or empirical practice?
3. `claim_support`
   - Are the main claims supported by theorems, identification, data, experiments, simulations, institutional evidence, or careful synthesis?
4. `technical_soundness`
   - Are the proof, identification strategy, estimation, experiment design, algorithm, or computational method credible for the paper type?
5. `literature_grounding`
   - Does the paper correctly position itself against closest substitutes, ancestors, method anchors, and absorption threats?
6. `evidence_strength`
   - Is the empirical, theoretical, computational, or documentary evidence strong enough for the stated contribution?
7. `reproducibility_transparency`
   - Are data, code, appendices, proofs, simulations, robustness checks, and implementation details inspectable enough for the claim?
8. `writing_clarity`
   - Can a target-field reader understand the question, contribution, evidence, and paper architecture without unnecessary friction?
9. `community_value`
   - Would the paper create useful knowledge, tools, facts, methods, benchmarks, or research directions for the relevant community?
10. `fatal_risk_severity`
   - How severe is the strongest fatal or near-fatal risk? Higher means more severe risk.

## Overall Scores

Provide two overall scores only after the dimension scores:

- `raw_overall_score`: the reviewer's direct 1-10 assessment before statistical calibration.
- `acceptance_likelihood_score`: a conservative 1-10 estimate of how likely a target-venue reviewer would be to recommend acceptance or revise-and-resubmit.

Keep these scores separate. A paper may have high diagnostic merit or community value but low acceptance likelihood because evidence is missing, claims are overstated, or the manuscript is not yet credible.

## Calibration Guidance

Before assigning `raw_overall_score >= 6`, require concrete support in at least these areas:

- clear contribution over closest literature;
- credible method, proof, identification, or evidence;
- sufficient target-field importance;
- no unresolved fatal risk.

Before assigning `raw_overall_score >= 7`, require strong evidence, clear positioning, and a best-case contribution that would plausibly matter to the target venue.

If the idea is interesting but evidence is thin, cap `raw_overall_score` at 5.5 unless the review explicitly explains why the missing evidence is nonessential.

If `fatal_risk_severity >= 8`, cap `acceptance_likelihood_score` at 4 unless the risk is explicitly provisional and likely resolvable with available appendix or supplemental evidence.

## Benchmark Use

For Ng-style benchmark comparisons, use the dimension scores as regression features and keep `raw_overall_score` as the uncalibrated baseline. Train any calibration model only on the training split and report test-set results separately.
