# Benchmark / Validation Mode

Use this file when the user asks to test, validate, benchmark, compare, or evaluate the reviewer skill.

## Benchmark Review Order

1. Hide final-version evidence from the reviewing pass when possible.
2. Read the early paper or supplied excerpt.
3. Classify the paper type and load the correct lens files.
4. Load `scorecard.md` if the benchmark requires numeric comparison with human reviewers.
5. Produce `must_not_miss_risks` before writing narrative prose.
6. Run the six-role panel.
7. For every severe criticism, run a false-fatal audit.
8. State what evidence would change the recommendation.
9. Only after the blind review, compare with final-version changes, public referee files, or human benchmark labels.

## Benchmark Output Schema

Use this structure for benchmark cases:

```text
case_id:
paper_type:
lenses_used:
central_economic_object:
must_not_miss_risks:
severe_or_fatal_risks:
false_fatal_audit:
evidence_needed_to_change_decision:
appendix_or_supplement_checked:
provisional_claims:
scorecard:
  originality:
  importance:
  claim_support:
  technical_soundness:
  literature_grounding:
  evidence_strength:
  reproducibility_transparency:
  writing_clarity:
  community_value:
  fatal_risk_severity:
  raw_overall_score:
  acceptance_likelihood_score:
  score_uncertainty:
final_version_alignment:
missed_risks:
false_fatal_criticisms:
professional_validity_score:
```

For Ng-style tests, keep this blind benchmark output fixed before opening human labels. Use the scorecard dimensions as calibration features. Train any linear regression or other calibrator only on the training split and report test-set performance separately from raw skill performance.

## False-Fatal Guardrail

A benchmark review should penalize both missed fatal risks and false fatal claims. A criticism is a false fatal risk if it would reject a paper even though:

- the paper's main contribution is descriptive but field-changing;
- the criticism is answered in an available appendix or supplement;
- the issue is a positioning problem rather than a validity problem;
- the paper's research design is appropriate for its actual claim;
- the paper documents an important economic object rather than estimating a clean causal effect or proving a theorem.

## Descriptive But Important Guardrail

Some economics papers make a professional contribution by documenting a robust fact, measurement pattern, institution, or puzzle. Before penalizing such a paper, ask:

- Is the documented fact credible?
- Does it change a model, policy calculation, field prior, or research agenda?
- Are alternative explanations considered?
- Is the evidence strong enough for the claim made?
- Does the paper overstate mechanism, welfare, or causality?

The review may still reject the paper if documentation is weak, if the fact is already known, or if implications are overstated. It should not reject merely because the paper is not a clean causal estimate or theorem paper.

## Appendix Discipline

Before finalizing a severe risk, check available appendices, proof sections, code notes, data appendices, and online supplements. If they are missing or inaccessible, say so explicitly and mark the risk provisional.
