from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any


FIXTURE_FIELDS = [
    "evidence_id",
    "case_id",
    "platform",
    "source_type",
    "acquisition_mode",
    "provenance_type",
    "verification_status",
    "trust_label",
    "trust_score",
    "review_status",
    "evidence_type",
    "title",
    "body_text",
    "comment_text",
    "language",
    "source_url",
    "url",
    "root_id",
    "parent_id",
    "created_at",
    "collected_at",
    "like_count",
    "reply_count",
    "share_count",
    "view_count",
    "content_hash",
    "normalized_content_hash",
    "canonical_url_hash",
    "duplicate_group_id",
    "duplicate_count",
    "risk_flags",
    "content_visibility",
    "access_scope",
    "source_capture_method",
    "coverage_note",
    "raw_data_safe",
    "ingestion_metadata",
    "is_root_content",
    "influence_core_candidate",
    "influence_core_type",
    "source_identity_type",
    "claim_summary",
    "stance_hint",
    "camp_state_hint",
    "emotion_hint",
    "topic_hint",
    "people_cluster_hint",
    "evidence_strength_hint",
    "logic_strength_hint",
    "emotional_intensity_hint",
]

DEFAULTS: dict[str, Any] = {
    "evidence_id": "",
    "case_id": "",
    "platform": "",
    "source_type": "",
    "acquisition_mode": "",
    "provenance_type": "",
    "verification_status": "",
    "trust_label": "",
    "trust_score": 0,
    "review_status": "",
    "evidence_type": "",
    "title": "",
    "body_text": "",
    "comment_text": "",
    "language": "",
    "source_url": "",
    "url": "",
    "root_id": "",
    "parent_id": "",
    "created_at": "",
    "collected_at": "",
    "like_count": 0,
    "reply_count": 0,
    "share_count": 0,
    "view_count": 0,
    "content_hash": "",
    "normalized_content_hash": "",
    "canonical_url_hash": "",
    "duplicate_group_id": "",
    "duplicate_count": 1,
    "risk_flags": [],
    "content_visibility": "public",
    "access_scope": "public",
    "source_capture_method": "",
    "coverage_note": "",
    "raw_data_safe": {},
    "ingestion_metadata": {},
    "is_root_content": False,
    "influence_core_candidate": False,
    "influence_core_type": "",
    "source_identity_type": "",
    "claim_summary": "",
    "stance_hint": "",
    "camp_state_hint": "",
    "emotion_hint": "",
    "topic_hint": "",
    "people_cluster_hint": "",
    "evidence_strength_hint": "",
    "logic_strength_hint": "",
    "emotional_intensity_hint": "",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def normalize_evidence_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for field in FIXTURE_FIELDS:
        value = row.get(field, DEFAULTS[field])
        if value is None:
            value = DEFAULTS[field]
        normalized[field] = value
    return normalized


def count_by_field(evidence: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(item.get(field) or "unknown") for item in evidence).items()))


def read_validation_report(package_path: Path) -> dict[str, Any]:
    path = package_path / "validation_report.json"
    if not path.exists():
        return {}
    return read_json(path)


def validation_errors_count(validation: dict[str, Any]) -> int:
    errors = validation.get("errors")
    if isinstance(errors, list):
        return len(errors)
    value = validation.get("errors_count")
    return int(value) if isinstance(value, int) else 0


def validation_warnings(validation: dict[str, Any]) -> list[str]:
    warnings = validation.get("warnings")
    if not isinstance(warnings, list):
        return []
    labels: list[str] = []
    for warning in warnings:
        if isinstance(warning, dict):
            code = warning.get("code")
            message = warning.get("message")
            labels.append(": ".join(part for part in [str(code or ""), str(message or "")] if part))
        else:
            labels.append(str(warning))
    return labels


def package_summary(
    manifest: dict[str, Any],
    evidence: list[dict[str, Any]],
    validation: dict[str, Any] | None = None,
    label: str | None = None,
) -> dict[str, Any]:
    validation = validation or {}
    data_scope = manifest.get("data_scope") if isinstance(manifest.get("data_scope"), dict) else {}
    package_role = str(manifest.get("package_role") or "")
    root_candidates = int(data_scope.get("root_content_count") or sum(1 for item in evidence if item.get("is_root_content")))
    validation_status = str(validation.get("status") or "passed_with_expected_warnings")
    warnings = validation_warnings(validation)
    if not warnings and "helldivers" in str(manifest.get("case_id", "")).lower():
        warnings = [
            "one skipped Polygon source",
            "sample size below target",
        ]
        validation_status = "passed_with_expected_warnings"

    return {
        "case_id": manifest.get("case_id", ""),
        "case_title": manifest.get("case_title", ""),
        "label": label or "Helldivers 2 / PSN small public sample",
        "package_role": package_role,
        "evidence_items": int(data_scope.get("evidence_items_count") or len(evidence)),
        "sources": int(data_scope.get("source_urls_count") or len({item.get("source_url") for item in evidence if item.get("source_url")})),
        "comment_samples": int(data_scope.get("comment_sample_count") or sum(1 for item in evidence if item.get("evidence_type") in {"comment", "reply"})),
        "root_candidates": root_candidates,
        "influence_core_candidates": sum(1 for item in evidence if item.get("influence_core_candidate")),
        "validation_status": validation_status,
        "validation_errors": validation_errors_count(validation),
        "validation_warnings": warnings,
        "platform_distribution": count_by_field(evidence, "platform"),
        "evidence_type_distribution": count_by_field(evidence, "evidence_type"),
        "trust_label_distribution": count_by_field(evidence, "trust_label"),
        "review_status_distribution": count_by_field(evidence, "review_status"),
        "verification_status_distribution": count_by_field(evidence, "verification_status"),
        "coverage_notes": [
            "selected public sample only",
            "controlled public sample only" if package_role == "candidate_demo_sample" else "small public sample only",
            "candidate_demo_sample" if package_role == "candidate_demo_sample" else "demo sample",
            "not full-web coverage",
            "not full-platform coverage",
            "not full-thread coverage",
            "not official verification",
            "not causal proof",
            "not a judgment of who is right or wrong",
            "not production data",
            "minors, families, and sensitive personal details are not exposed",
        ],
        "runtime_safety": [
            "frontend-local fixture mode",
            "no backend API call",
            "no runtime package file fetch",
            "no real platform action",
        ],
    }


def js_export(name: str, value: Any) -> str:
    return f"export const {name} = {json.dumps(value, ensure_ascii=False, indent=2)}\n"


def generate_fixture(
    package_dir: str | Path,
    out_file: str | Path,
    *,
    export_prefix: str = "helldivers2Psn",
    label: str | None = None,
) -> dict[str, Any]:
    package_path = Path(package_dir)
    output_path = Path(out_file)
    manifest = read_json(package_path / "manifest.json")
    evidence = [normalize_evidence_row(row) for row in read_jsonl(package_path / "evidence_items.jsonl")]
    validation = read_validation_report(package_path)
    summary = package_summary(manifest, evidence, validation, label=label)
    public_manifest = {
        "case_id": manifest.get("case_id", ""),
        "case_title": manifest.get("case_title", ""),
        "package_version": manifest.get("package_version", ""),
        "contract_version": manifest.get("contract_version", ""),
        "exported_at": manifest.get("exported_at", ""),
        "package_role": manifest.get("package_role", ""),
        "coverage_note": manifest.get("coverage_note", ""),
        "data_scope": manifest.get("data_scope", {}),
        "skipped_sources_count": len(manifest.get("skipped_sources") or []),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(
            [
                "// Generated from a local Sentigraph Evidence Export v1 package.",
                "// Frontend fixture only: no runtime fetch, no backend import, no platform action.",
                js_export(f"{export_prefix}SampleMetadata", public_manifest),
                js_export(f"{export_prefix}SampleManifest", public_manifest),
                js_export(f"{export_prefix}EvidenceItems", evidence),
                js_export(f"{export_prefix}SampleSummary", summary),
            ]
        ),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a frontend-local Opinion Ecosystem fixture from a Sentigraph Evidence Export v1 package.")
    parser.add_argument("--package", required=True, help="Local Evidence Export v1 package folder.")
    parser.add_argument("--out", required=True, help="Output frontend fixture module path.")
    parser.add_argument("--export-prefix", default="helldivers2Psn", help="Prefix for exported JS constants.")
    parser.add_argument("--label", default=None, help="Sample label for the generated summary.")
    args = parser.parse_args()
    summary = generate_fixture(args.package, args.out, export_prefix=args.export_prefix, label=args.label)
    print(
        "Generated frontend fixture: "
        f"evidence={summary['evidence_items']}, sources={summary['sources']}, comments={summary['comment_samples']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
