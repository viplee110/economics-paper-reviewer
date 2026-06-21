#!/usr/bin/env python3
"""Fit a train/test linear calibration model for reviewer scorecards."""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any


FEATURES = [
    "originality",
    "importance",
    "claim_support",
    "technical_soundness",
    "literature_grounding",
    "evidence_strength",
    "reproducibility_transparency",
    "writing_clarity",
    "community_value",
    "fatal_risk_severity",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def get_truth_rows(path: Path) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    if isinstance(data, dict):
        if "cases" in data:
            data = data["cases"]
        elif "data" in data:
            data = data["data"]
        else:
            data = list(data.values())
    return {row["case_id"]: row for row in data}


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    vx = sum((a - mx) ** 2 for a in x)
    vy = sum((b - my) ** 2 for b in y)
    if vx == 0 or vy == 0:
        return float("nan")
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(vx * vy)


def ranks(values: list[float]) -> list[float]:
    pairs = sorted((value, idx) for idx, value in enumerate(values))
    out = [0.0] * len(values)
    i = 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        avg = (i + 1 + j) / 2
        for _, idx in pairs[i:j]:
            out[idx] = avg
        i = j
    return out


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(ranks(x), ranks(y))


def auc(labels: list[bool], scores: list[float]) -> float:
    pos = [s for label, s in zip(labels, scores) if label]
    neg = [s for label, s in zip(labels, scores) if not label]
    if not pos or not neg:
        return float("nan")
    total = 0
    good = 0.0
    for p in pos:
        for n in neg:
            total += 1
            if p > n:
                good += 1
            elif p == n:
                good += 0.5
    return good / total


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix)]


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    b_t = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in b_t] for row in a]


def matvec(a: list[list[float]], x: list[float]) -> list[float]:
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(a)
    aug = [row[:] + [b_i] for row, b_i in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [x / div for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[-1] for row in aug]


def fit_ols(x_rows: list[list[float]], y: list[float], ridge: float = 1e-6) -> list[float]:
    x = [[1.0] + row for row in x_rows]
    xt = transpose(x)
    xtx = matmul(xt, x)
    for i in range(len(xtx)):
        xtx[i][i] += ridge
    xty = matvec(xt, y)
    return solve_linear(xtx, xty)


def predict(beta: list[float], x_rows: list[list[float]]) -> list[float]:
    return [beta[0] + sum(b * x for b, x in zip(beta[1:], row)) for row in x_rows]


def metrics(y_true: list[float], y_pred: list[float], accepted: list[bool]) -> dict[str, float]:
    err = [p - y for p, y in zip(y_pred, y_true)]
    return {
        "pearson": pearson(y_pred, y_true),
        "spearman": spearman(y_pred, y_true),
        "mae": sum(abs(e) for e in err) / len(err),
        "rmse": math.sqrt(sum(e * e for e in err) / len(err)),
        "mean_prediction": sum(y_pred) / len(y_pred),
        "mean_human": sum(y_true) / len(y_true),
        "bias_prediction_minus_human": sum(err) / len(err),
        "accepted_auc": auc(accepted, y_pred),
    }


def bootstrap_ci(y_true: list[float], y_pred: list[float], accepted: list[bool], seed: int, n_boot: int) -> dict[str, list[float]]:
    rng = random.Random(seed)
    out: dict[str, list[float]] = {"pearson": [], "spearman": [], "accepted_auc": []}
    n = len(y_true)
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        yt = [y_true[i] for i in idx]
        yp = [y_pred[i] for i in idx]
        ac = [accepted[i] for i in idx]
        out["pearson"].append(pearson(yp, yt))
        out["spearman"].append(spearman(yp, yt))
        out["accepted_auc"].append(auc(ac, yp))
    ci = {}
    for key, values in out.items():
        clean = sorted(v for v in values if v == v)
        if clean:
            ci[key] = [clean[int(0.025 * (len(clean) - 1))], clean[int(0.975 * (len(clean) - 1))]]
        else:
            ci[key] = [float("nan"), float("nan")]
    return ci


def build_rows(reviews: list[dict[str, Any]], truth: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for review in reviews:
        case_id = review["case_id"]
        if case_id not in truth:
            continue
        scorecard = review["scorecard"]
        rows.append(
            {
                "case_id": case_id,
                "features": [float(scorecard[field]) for field in FEATURES],
                "raw_overall_score": float(scorecard["raw_overall_score"]),
                "acceptance_likelihood_score": float(scorecard["acceptance_likelihood_score"]),
                "human_mean_rating": float(truth[case_id]["human_mean_rating"]),
                "accepted": str(truth[case_id].get("status", "")).lower() == "accepted",
                "status": truth[case_id].get("status"),
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews", required=True, type=Path, help="Blind reviews JSONL with scorecards.")
    parser.add_argument("--truth", required=True, type=Path, help="Hidden truth JSON opened only after blind lock.")
    parser.add_argument("--train-size", type=int, default=150)
    parser.add_argument("--seed", type=int, default=110057)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--split", type=Path, default=None, help="Optional existing split JSON.")
    parser.add_argument("--write-split", type=Path, default=None, help="Optional path to write the split JSON.")
    parser.add_argument("--report", type=Path, default=None, help="Output metrics JSON.")
    args = parser.parse_args()

    reviews = load_jsonl(args.reviews)
    truth = get_truth_rows(args.truth)
    rows = build_rows(reviews, truth)
    if len(rows) <= args.train_size:
        raise SystemExit(f"not enough joined rows for train-size {args.train_size}: {len(rows)}")

    if args.split:
        split = load_json(args.split)
        train_ids = split["train_ids"]
        test_ids = split["test_ids"]
    else:
        rng = random.Random(args.seed)
        ids = [row["case_id"] for row in rows]
        rng.shuffle(ids)
        train_ids = ids[: args.train_size]
        test_ids = ids[args.train_size :]
        split = {"seed": args.seed, "train_size": args.train_size, "train_ids": train_ids, "test_ids": test_ids}

    row_by_id = {row["case_id"]: row for row in rows}
    train = [row_by_id[case_id] for case_id in train_ids if case_id in row_by_id]
    test = [row_by_id[case_id] for case_id in test_ids if case_id in row_by_id]

    beta = fit_ols([row["features"] for row in train], [row["human_mean_rating"] for row in train])

    def eval_set(dataset: list[dict[str, Any]]) -> dict[str, Any]:
        y = [row["human_mean_rating"] for row in dataset]
        raw = [row["raw_overall_score"] for row in dataset]
        acceptance = [row["acceptance_likelihood_score"] for row in dataset]
        calibrated = predict(beta, [row["features"] for row in dataset])
        accepted = [row["accepted"] for row in dataset]
        return {
            "n": len(dataset),
            "raw_overall": metrics(y, raw, accepted),
            "acceptance_likelihood": metrics(y, acceptance, accepted),
            "calibrated": metrics(y, calibrated, accepted),
            "calibrated_bootstrap_95ci": bootstrap_ci(y, calibrated, accepted, args.seed + 1, args.bootstrap),
        }

    report = {
        "reviews": str(args.reviews),
        "truth": str(args.truth),
        "features": FEATURES,
        "split": split,
        "coefficients": {"intercept": beta[0], **{feature: value for feature, value in zip(FEATURES, beta[1:])}},
        "train": eval_set(train),
        "test": eval_set(test),
        "status_counts": {status: sum(1 for row in rows if row["status"] == status) for status in sorted({row["status"] for row in rows})},
    }

    if args.write_split:
        args.write_split.parent.mkdir(parents=True, exist_ok=True)
        args.write_split.write_text(json.dumps(split, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
