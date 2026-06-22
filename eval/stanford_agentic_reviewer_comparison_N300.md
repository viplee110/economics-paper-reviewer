# Full-Text Benchmark Comparison With Stanford Agentic Reviewer

This document reports a public-safe benchmark summary for the `economics-paper-reviewer` skill. It compares our observed full-text review-score performance with the headline metrics reported by Stanford Agentic Reviewer / PaperReview.ai.

This is a benchmark report, not a dataset release. Raw PDFs, extracted paper text, hidden labels, and per-paper review outputs are not committed to this repository.

## Executive Summary

We ran a blind full-text benchmark on 300 randomly sampled ICLR 2026 OpenReview submissions with public PDFs and human reviewer ratings.

The skill completed 300 out of 300 full-text reviews before hidden human labels were opened. Its scores correlated strongly with human reviewer ratings:

```text
AI acceptance_likelihood_score vs mean human rating:
  Pearson  = 0.719
  Spearman = 0.713

AI acceptance_likelihood_score vs individual human rating:
  Pearson  = 0.496
  Spearman = 0.486

Single human reviewer vs other reviewers' mean:
  Pearson  = 0.405
  Spearman = 0.394

150/150 train-test linear scorecard:
  Test Pearson  = 0.775
  Test Spearman = 0.778
```

The skill's AI-vs-individual-human Spearman correlation (`0.486`) is above the single-human-vs-other-humans Spearman correlation (`0.394`) in the same sample. This is encouraging evidence that the skill's structured scorecard captures meaningful peer-review signal.

However, this benchmark uses machine-learning conference papers, not economics papers. It supports pipeline and cross-domain academic review validity, but it does not establish economics-domain professional referee validity.

## System Under Evaluation

The evaluated system is `economics-paper-reviewer`, a portable reviewer skill for English economics papers. Its canonical protocol uses a six-role panel:

1. Referee 1: primary-field specialist.
2. Referee 2: closest-literature / adjacent-field specialist.
3. Referee 3: method / mechanism / application / institutional specialist.
4. Referee 4: rigor / reproducibility specialist.
5. Referee 5: Scientific Judge / Idea Critic.
6. Referee 6: Advocate / Best-Case Reader.

The skill classifies papers into type lenses:

- theory;
- empirical causal;
- structural / IO empirical;
- econometrics / methodology;
- experimental / behavioral;
- computational / simulation;
- survey / literature review;
- mixed.

For this benchmark, the test papers were ICLR machine-learning papers, so the review mostly exercised the computational / methodology lens.

## Benchmark Design

### Data

```text
Source: ICLR 2026 OpenReview public submissions
Eligible public reviewed papers found: 380
Random sample size: 300
Random seed: 110057
PDFs downloaded and extracted: 300/300
Blind full-text reviews completed: 300/300
Scorecard validation bad_count: 0
Individual human ratings: 1170
```

Status distribution:

```text
accepted: 49
rejected: 131
desk_rejected: 19
withdrawn: 101
```

### Blind Protocol

1. Fetch public OpenReview metadata and PDFs.
2. Extract full text.
3. Generate blind review inputs.
4. Produce one full-text review and one JSON scorecard for every paper.
5. Validate all 300 scorecards.
6. Only after validation, open hidden human labels.
7. Join skill scores to human review ratings.
8. Compute correlation, train-test calibration, and AUC metrics.

No human ratings, human decisions, or OpenReview review text were used during the blind review phase.

## Scorecard

The skill generated these score dimensions:

```text
originality
importance
claim_support
technical_soundness
literature_grounding
evidence_strength
reproducibility_transparency
writing_clarity
community_value
fatal_risk_severity
raw_overall_score
acceptance_likelihood_score
```

The main raw skill score is `acceptance_likelihood_score`. The train-test calibration uses the ten component dimensions and predicts mean human rating.

## Results

### Skill Score vs Mean Human Rating

```text
acceptance_likelihood_score:
  Pearson:  0.719
  Spearman: 0.713
  Pearson 95% CI: [0.659, 0.769]
  p-value approximation: 8.31e-55

raw_overall_score:
  Pearson:  0.701
  Spearman: 0.700
  Pearson 95% CI: [0.638, 0.754]
  p-value approximation: 1.18e-50
```

### Dimension-Level Pearson Correlations

```text
originality:                  0.635
importance:                   0.582
claim_support:                0.675
technical_soundness:          0.659
literature_grounding:         0.634
evidence_strength:            0.677
reproducibility_transparency: 0.672
writing_clarity:              0.649
community_value:              0.663
fatal_risk_severity:         -0.664
```

The signs are coherent: positive quality dimensions correlate positively with human ratings, while fatal-risk severity correlates negatively.

### Ng-Style Comparable Metrics

To approximate the Stanford Agentic Reviewer framing, we compare the AI score against individual human reviewer ratings. We also compare a single human reviewer against the mean of the other reviewers for the same paper.

```text
AI acceptance_likelihood_score vs individual human rating:
  Pearson:  0.496
  Spearman: 0.486
  Spearman 95% CI: [0.441, 0.528]

AI raw_overall_score vs individual human rating:
  Pearson:  0.485
  Spearman: 0.477
  Spearman 95% CI: [0.432, 0.520]

Single human reviewer vs other reviewers' mean:
  Pearson:  0.405
  Spearman: 0.394
  Spearman 95% CI: [0.344, 0.441]
```

### Train/Test Linear Scorecard

We followed the general idea of learning a simple linear mapping from scorecard dimensions to human mean rating.

```text
Train/test split seed: 110057
Train N: 150
Test N: 150

Test Pearson:  0.775
Test Spearman: 0.778
Test Pearson 95% CI: [0.702, 0.832]
```

### Acceptance Prediction

Using accepted papers as positive and rejected, desk-rejected, or withdrawn papers as negative:

```text
accepted N: 49
non-accepted N: 251

AUC using acceptance_likelihood_score: 0.950
AUC using raw_overall_score:         0.926
```

The AUC is high, but it should be interpreted cautiously because withdrawn and desk-rejected papers make classification easier than a strict accepted-vs-borderline-rejected benchmark.

## Comparison With Stanford Agentic Reviewer / PaperReview.ai

The Stanford Agentic Reviewer technical overview reports an ICLR 2025 benchmark with a 150-submission training set and a 147-submission test set. Their headline metrics include:

```text
Spearman correlation between two human reviewers: 0.41
Spearman correlation between AI score and one human score: 0.42
AUC for predicting acceptance using one human score: 0.84
AUC using the AI score: 0.75
```

Source: [Stanford Agentic Reviewer / PaperReview.ai Technical Overview](https://paperreview.ai/tech-overview).

| Metric | Stanford Agentic Reviewer / PaperReview.ai | Economics Paper Reviewer Skill |
|---|---:|---:|
| Dataset | ICLR 2025 | ICLR 2026 |
| Train/test setup | 150 train / 147 test | 150 train / 150 test |
| AI vs one-human Spearman | 0.42 | 0.486 |
| Human-human Spearman | 0.41 | 0.394 |
| AI AUC for acceptance | 0.75 | 0.950 |
| AI vs mean-human Spearman | not headline metric | 0.713 |
| Calibrated test Spearman | not directly comparable from public summary | 0.778 |

The skill is competitive with the public Stanford Agentic Reviewer headline metrics and is stronger on the closest available AI-vs-individual-human Spearman metric in this benchmark. The AUC comparison is less reliable because the datasets and label distributions differ.

## Over-Strictness Diagnostic

A useful reviewer should be critical, but not indiscriminately severe. We therefore ran a simple over-strictness diagnostic on the N=300 benchmark: if the skill were uniformly too harsh, we would expect many human-accepted papers to receive very low scores.

Accepted papers:

```text
n: 49
acceptance_likelihood_score mean: 6.647
acceptance_likelihood_score median: 7.0
minimum: 4.0
maximum: 7.4
share below 5: 2.0%
share below 6: 8.2%
```

Non-accepted papers:

```text
n: 251
acceptance_likelihood_score mean: 4.367
acceptance_likelihood_score median: 4.5
minimum: 1.5
maximum: 6.8
share below 5: 59.8%
share below 6: 84.9%
```

This diagnostic does not show a simple pattern of uniform over-strictness. The skill did not systematically assign very low scores to papers that human reviewers accepted. That said, this does not prove that every criticism or revision suggestion is beneficial. False-fatal and over-conservative revision risks require a separate revision-impact benchmark.

## What This Benchmark Supports

The benchmark supports these claims:

1. The skill can complete full-text review at 300-paper scale.
2. Its scorecard dimensions are numerically coherent.
3. Its scores strongly correlate with mean human reviewer ratings in a cross-domain peer-review benchmark.
4. Its AI-vs-individual-human correlation is comparable to, and in this sample higher than, human-vs-human agreement.
5. A simple linear calibration over scorecard dimensions predicts held-out human ratings.
6. The skill is useful as a structured pre-review assistant.

## What This Benchmark Does Not Support

The benchmark does not establish:

1. economics-domain professional referee validity;
2. correctness of theorem verification;
3. correctness of causal identification judgments;
4. structural estimation validity;
5. equilibrium-proof validity;
6. novelty certification;
7. journal acceptance prediction for economics journals;
8. replacement of human economists or referees.

The correct interpretation is:

```text
The skill has meaningful peer-review signal and is ready for serious pre-review assistance.
It is not yet validated as a professional economics referee.
The next milestone is an economics-specific benchmark.
```

## Threats To Validity

### Domain Shift

The benchmark uses machine-learning conference papers. Economics review requires different forms of judgment:

- economic mechanism clarity;
- model primitives;
- identification strategy;
- exclusion restrictions;
- equilibrium concepts;
- welfare interpretation;
- structural estimation assumptions;
- institutional relevance;
- closest economics literature.

### Status Leakage

At least one blind input contained status-like metadata in the paper text itself. Hidden labels were not used during review generation, but future benchmark extraction should strip publication and status metadata.

### Label Construction

Human ratings are noisy. A mean human rating is not identical to a final editorial decision, and a single reviewer is an imperfect benchmark. The human-vs-human statistic partly quantifies this noise.

### Classification Inflation

The AUC statistic includes withdrawn and desk-rejected papers as negatives. That likely inflates separability relative to a strict accepted-vs-borderline-rejected benchmark.

### Manual Agentic Execution

The benchmark used the skill protocol in a controlled agentic execution rather than a fully locked deterministic runner. Future public benchmarks should fix model, prompts, extraction, scoring code, and calibration before running.

### Literature Verification Limits

External literature search was not performed for every paper in this 300-paper benchmark. The test emphasizes full-text review judgment more than search-grounded novelty verification.

## Next Step: Economics-Specific Validity

The next scientific benchmark should use economics papers. Good designs include:

1. Early working paper vs final published version comparisons.
2. Public peer-review files for economics-related papers.
3. Expert-labeled economics manuscripts.
4. Published-paper controls to measure false-fatal risk.
5. Field-specific tests for theory, empirical causal, structural IO, econometrics, and experimental economics.

The most informative benchmark would ask:

```text
Does the skill identify the same fatal and fixable risks that real economics referees, editors, or later published revisions reveal?
```

## Bottom Line

The N=300 full-text benchmark is a strong first validation of the `economics-paper-reviewer` skill as a general academic review protocol. On ICLR 2026 submissions, the skill's score correlates with mean human rating at Spearman `0.713`, and its individual-review comparison reaches Spearman `0.486`, above the single-human-vs-other-humans Spearman `0.394` in the same sample. A simple train/test linear calibration achieves test Spearman `0.778`.

Compared with the public Stanford Agentic Reviewer / PaperReview.ai headline results, the skill is competitive and appears stronger on this particular benchmark. The comparison is not definitive because the datasets, label distributions, and execution settings differ.

The skill should be described as a structured academic pre-review assistant with promising benchmark validity, not as an acceptance oracle or substitute for expert economics judgment.
