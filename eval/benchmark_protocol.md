# Ng-Style Full-Text Benchmark Protocol

This protocol defines the public, reproducible benchmark design for testing the `economics-paper-reviewer` skill against human reviewer ratings.

The goal is to reproduce the evaluation shape of Stanford Agentic Reviewer as closely as possible while keeping the economics reviewer skill's protocol fixed and auditable.

## Core Standard

This benchmark is full-text.

Do not use abstract-only or excerpt-only review for the main benchmark. Those are pilot tests and must be labeled as such.

Every benchmark paper must receive:

1. full paper text extraction;
2. status-leak audit;
3. related-work grounding when tools are available;
4. full skill review;
5. six-role panel;
6. false-fatal audit;
7. complete scorecard;
8. blind lock before human labels are opened.

## Protocol Freeze

Before starting the benchmark, record:

- skill repository commit hash;
- benchmark protocol commit hash;
- date and time;
- model / IDE used for review;
- scorecard schema version;
- random seed;
- planned sample size;
- train/test split rule.

Do not tune prompts, dimensions, weights, thresholds, or review instructions after seeing human labels.

## Sample Construction

Target shape:

- `N = 300` full-text papers for blind review;
- `150` papers for calibration training;
- remaining papers for held-out testing.

If the source dataset has missing human ratings, record exclusions before opening scores for analysis.

Recommended public source:

- OpenReview conference submissions with public PDFs and reviewer ratings.

Record each case in `sample_manifest.csv`:

```text
case_id
source
forum_id
title
pdf_url
submission_version
sample_seed
sample_stratum
download_status
license_or_access_note
```

Do not commit downloaded PDFs or extracted copyrighted full text.

## Full-Text Extraction

For every paper, extract text from the full PDF, including appendices when available.

Record `extraction_log.csv`:

```text
case_id
pdf_status
text_status
full_text_word_count
appendix_detected
table_or_figure_loss_risk
math_extraction_risk
status_leak_detected
status_leak_notes
text_hash
```

Minimum rule for the main benchmark:

- `text_status = ok`;
- `full_text_word_count` should usually exceed 3000;
- any paper below the threshold must be manually justified or excluded.

## Blinding And Leak Control

Before blind review, remove or mask:

- final decision;
- acceptance / rejection / withdrawn language;
- venue status;
- camera-ready status;
- author response status;
- public review outcome;
- metadata fields such as `venueid` that encode outcome.

Keep a separate hidden truth file. Do not open it until all blind scorecards pass validation.

## Related-Work Grounding

For each paper, record related-work grounding in `related_work_log.jsonl`:

```json
{
  "case_id": "C001",
  "queries": [],
  "related_papers": [
    {
      "title": "",
      "source": "",
      "access_level": "metadata|abstract|full_text",
      "relation": "closest substitute|method anchor|baseline|adjacent",
      "confidence": "low|medium|high"
    }
  ],
  "grounding_limitations": []
}
```

If search is unavailable, mark related-work and literature-grounding scorecard fields provisional.

## Blind Review Schema

Write one JSON object per paper to `blind_reviews.jsonl`.

Minimum required fields:

```json
{
  "case_id": "C001",
  "skill_commit": "",
  "protocol_commit": "",
  "model_or_ide": "",
  "input_text_hash": "",
  "full_text_word_count": 0,
  "paper_type": "",
  "paper_type_confidence": "",
  "lenses_used": [],
  "related_work_grounding": {},
  "must_not_miss_risks": [],
  "six_role_panel": {
    "referee_1_primary_field": "",
    "referee_2_closest_literature": "",
    "referee_3_method_mechanism_application": "",
    "referee_4_rigor_reproducibility": "",
    "referee_5_scientific_judge": "",
    "referee_6_advocate": ""
  },
  "fatal_risks": [],
  "fixable_risks": [],
  "false_fatal_audit": "",
  "manuscript_architecture_diagnosis": "",
  "recommendation_range": "",
  "scorecard": {
    "originality": 0,
    "importance": 0,
    "claim_support": 0,
    "technical_soundness": 0,
    "literature_grounding": 0,
    "evidence_strength": 0,
    "reproducibility_transparency": 0,
    "writing_clarity": 0,
    "community_value": 0,
    "fatal_risk_severity": 0,
    "raw_overall_score": 0,
    "acceptance_likelihood_score": 0
  },
  "score_uncertainty": "",
  "provisional_score_fields": []
}
```

Do not include human labels or final outcome fields in `blind_reviews.jsonl`.

## Blind Lock

Before opening the hidden truth file:

1. validate one scorecard per case;
2. validate no duplicate case ids;
3. validate no missing scorecard fields;
4. validate score ranges;
5. validate full-text word-count threshold;
6. validate no forbidden human-label fields;
7. write a validation report;
8. hash the blind review file.

Only after this lock may human labels be loaded.

## Calibration Design

Report raw skill performance first.

Then train a calibration model on the training split only:

```text
human_mean_rating ~ scorecard dimensions
```

The default feature set is:

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
```

Do not include `raw_overall_score` or `acceptance_likelihood_score` in the default calibration unless a separate robustness table reports it.

## Required Metrics

Report all metrics on the held-out test set:

- Pearson correlation with human mean rating;
- Spearman correlation with human mean rating;
- bootstrap 95% confidence intervals;
- MAE and RMSE;
- acceptance AUC when accepted/rejected labels are available;
- human-human reliability when individual reviewer ratings are available;
- false-positive and false-negative cases;
- status-leak clean subset;
- score calibration bias.

Report raw and calibrated results separately.

## Benchmark Article

After the benchmark, write a short public article:

1. what was tested;
2. how the benchmark reproduces Stanford Agentic Reviewer's evaluation shape;
3. data and blinding;
4. full-text review pipeline;
5. scorecard and calibration;
6. main results;
7. error analysis;
8. limitations;
9. implications for economics paper review;
10. next economics-specific benchmark.

Use `eval/scripts/write_benchmark_article.py` to generate the first draft from the metrics JSON, then edit the prose for public release.

## Public Release Policy

Commit:

- protocol;
- scripts;
- aggregate metrics;
- sanitized reports;
- case ids and metadata when legally safe.

Do not commit:

- PDFs;
- extracted full text;
- copyrighted paper text;
- raw review text if it quotes long passages;
- hidden labels before the blind lock;
- any file that encodes status leaks into review inputs.
