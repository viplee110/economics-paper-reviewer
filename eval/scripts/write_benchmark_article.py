#!/usr/bin/env python3
"""Write a concise public benchmark article from calibration metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def metric_table(metrics: dict[str, Any], label: str) -> str:
    rows = []
    for score_name in ["raw_overall", "acceptance_likelihood", "calibrated"]:
        block = metrics[score_name]
        rows.append(
            f"| {label} {score_name} | {fmt(block['pearson'])} | {fmt(block['spearman'])} | "
            f"{fmt(block['accepted_auc'])} | {fmt(block['mae'])} | {fmt(block['rmse'])} | "
            f"{fmt(block['bias_prediction_minus_human'])} |"
        )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", required=True, type=Path, help="Metrics JSON from fit_calibrator.py.")
    parser.add_argument("--output", required=True, type=Path, help="Output Markdown article.")
    parser.add_argument("--skill-commit", default="", help="Skill commit hash used for blind review.")
    parser.add_argument("--protocol-commit", default="", help="Benchmark protocol commit hash.")
    parser.add_argument("--sample-note", default="Full-text OpenReview-style benchmark.", help="Brief sample description.")
    args = parser.parse_args()

    data = load_json(args.metrics)
    test = data["test"]
    train = data["train"]
    split = data["split"]
    features = ", ".join(data["features"])

    article = f"""# Full-Text Reviewer Skill Benchmark

## Summary

This benchmark evaluates the `economics-paper-reviewer` skill as a full-text reviewer protocol. The test follows an Ng-style design: blind full-text reviews are completed first, scorecard dimensions are extracted, human labels remain hidden until blind lock, and a linear calibration model is trained only on the training split before held-out testing.

This benchmark tests reviewer-protocol validity and score calibration. It does not by itself prove professional economics-review validity unless the sample is economics-specific.

## Protocol

- Skill commit: `{args.skill_commit or 'not recorded'}`
- Protocol commit: `{args.protocol_commit or 'not recorded'}`
- Sample: {args.sample_note}
- Training size: {split.get('train_size')}
- Test size: {len(split.get('test_ids', []))}
- Random seed: {split.get('seed')}
- Calibration features: {features}

## Benchmark Discipline

The benchmark uses full paper text, not abstract-only or excerpt-only inputs. Each paper must pass scorecard validation before human labels are opened. Raw skill scores and calibrated test-set scores are reported separately.

## Main Metrics

| Score | Pearson | Spearman | Acceptance AUC | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|---:|---:|
{metric_table(train, 'train')}
{metric_table(test, 'test')}

## Calibration Model

The linear calibration model predicts human mean reviewer ratings from the scorecard dimensions. Coefficients should be interpreted as calibration weights, not causal estimates of review quality.

```json
{json.dumps(data['coefficients'], indent=2)}
```

## Interpretation

Raw reviewer scores measure the skill's uncalibrated judgment. Calibrated scores measure whether the scorecard dimensions contain enough signal to predict human reviewer ratings after a simple linear mapping is learned on the training split.

When reporting results publicly, emphasize the held-out test metrics. Training metrics are useful only for diagnosing overfit or calibration behavior.

## Limitations

- Human reviewer ratings are noisy and may have limited inter-reviewer reliability.
- Acceptance outcomes partly reflect human review scores, so acceptance AUC is not an independent construct-validity measure.
- Any status-leak subset must be reported separately.
- Cross-domain benchmarks do not establish economics professional validity.
- Economics-specific validation requires economics papers and economics-relevant human or publication-path evidence.

## Next Steps

1. Inspect false positives and false negatives.
2. Compare raw and calibrated score distributions.
3. Report clean no-status-leak subset metrics.
4. Run an economics-specific validity benchmark using legally clean working-paper/final-version or public peer-review evidence.
"""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(article, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
