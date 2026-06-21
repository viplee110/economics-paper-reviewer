#!/usr/bin/env python3
"""Validate full-text blind-review scorecards before human labels are opened."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCORECARD_FIELDS = [
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
    "raw_overall_score",
    "acceptance_likelihood_score",
]

PANEL_FIELDS = [
    "referee_1_primary_field",
    "referee_2_closest_literature",
    "referee_3_method_mechanism_application",
    "referee_4_rigor_reproducibility",
    "referee_5_scientific_judge",
    "referee_6_advocate",
]

REQUIRED_TOP_LEVEL = [
    "case_id",
    "skill_commit",
    "protocol_commit",
    "input_text_hash",
    "full_text_word_count",
    "paper_type",
    "lenses_used",
    "related_work_grounding",
    "must_not_miss_risks",
    "six_role_panel",
    "fatal_risks",
    "fixable_risks",
    "false_fatal_audit",
    "manuscript_architecture_diagnosis",
    "recommendation_range",
    "scorecard",
]

ALLOW_EMPTY_TOP_LEVEL = {
    "fatal_risks",
    "fixable_risks",
    "provisional_score_fields",
}

FORBIDDEN_LABEL_FIELDS = {
    "human_mean_rating",
    "human_rating",
    "human_score",
    "ratings",
    "review_ratings",
    "acceptance",
    "accepted",
    "rejected",
    "withdrawn",
    "decision",
    "decision_note",
    "final_decision",
    "venueid",
    "venue_id",
    "venue",
    "status",
}

ALLOWED_STATUS_FIELDS = {
    "pdf_status",
    "text_status",
    "extraction_status",
    "status_leak_detected",
    "status_leak_notes",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(obj, dict):
                raise SystemExit(f"{path}:{lineno}: expected JSON object")
            rows.append(obj)
    return rows


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_forbidden(obj: Any, path: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            child_path = f"{path}.{key}" if path else str(key)
            if key_lower in FORBIDDEN_LABEL_FIELDS and key_lower not in ALLOWED_STATUS_FIELDS:
                hits.append(child_path)
            hits.extend(walk_forbidden(value, child_path))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            hits.extend(walk_forbidden(value, f"{path}[{idx}]"))
    return hits


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def validate_row(row: dict[str, Any], min_word_count: int, require_related_work: bool) -> list[str]:
    errors: list[str] = []
    case_id = row.get("case_id", "<missing>")

    for field in REQUIRED_TOP_LEVEL:
        if field not in row:
            errors.append(f"{case_id}: missing top-level field {field}")
        elif field not in ALLOW_EMPTY_TOP_LEVEL and not nonempty(row[field]):
            errors.append(f"{case_id}: empty top-level field {field}")

    word_count = row.get("full_text_word_count")
    if not isinstance(word_count, (int, float)) or word_count < min_word_count:
        errors.append(f"{case_id}: full_text_word_count below threshold {min_word_count}: {word_count}")

    scorecard = row.get("scorecard")
    if isinstance(scorecard, dict):
        for field in SCORECARD_FIELDS:
            if field not in scorecard:
                errors.append(f"{case_id}: missing scorecard field {field}")
                continue
            value = scorecard[field]
            if not isinstance(value, (int, float)):
                errors.append(f"{case_id}: nonnumeric scorecard field {field}: {value!r}")
            elif not (1 <= float(value) <= 10):
                errors.append(f"{case_id}: scorecard field {field} out of 1-10 range: {value}")
    else:
        errors.append(f"{case_id}: scorecard is not an object")

    panel = row.get("six_role_panel")
    if isinstance(panel, dict):
        for field in PANEL_FIELDS:
            if not nonempty(panel.get(field)):
                errors.append(f"{case_id}: missing or empty panel field {field}")
    else:
        errors.append(f"{case_id}: six_role_panel must be an object with six referee fields")

    if require_related_work:
        grounding = row.get("related_work_grounding")
        if not isinstance(grounding, dict):
            errors.append(f"{case_id}: related_work_grounding must be an object")
        else:
            related = grounding.get("related_papers") or grounding.get("related_work") or []
            limitations = grounding.get("grounding_limitations") or []
            if not related and not limitations:
                errors.append(f"{case_id}: related_work_grounding has neither related papers nor limitations")

    forbidden_hits = walk_forbidden(row)
    if forbidden_hits:
        errors.append(f"{case_id}: forbidden human-label/status fields present: {', '.join(forbidden_hits[:8])}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews", required=True, type=Path, help="Blind review JSONL file.")
    parser.add_argument("--expected-n", type=int, default=None, help="Expected number of cases.")
    parser.add_argument("--min-word-count", type=int, default=3000, help="Minimum full-text word count.")
    parser.add_argument("--allow-missing-related-work", action="store_true", help="Allow missing related-work grounding.")
    parser.add_argument("--report", type=Path, default=None, help="Optional JSON validation report path.")
    args = parser.parse_args()

    rows = load_jsonl(args.reviews)
    ids = [row.get("case_id") for row in rows]
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    errors: list[str] = []

    if args.expected_n is not None and len(rows) != args.expected_n:
        errors.append(f"expected {args.expected_n} rows, found {len(rows)}")
    if duplicates:
        errors.append(f"duplicate case ids: {duplicates}")

    for row in rows:
        errors.extend(validate_row(row, args.min_word_count, not args.allow_missing_related_work))

    report = {
        "reviews": str(args.reviews),
        "sha256": sha256_file(args.reviews),
        "n_rows": len(rows),
        "expected_n": args.expected_n,
        "min_word_count": args.min_word_count,
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
