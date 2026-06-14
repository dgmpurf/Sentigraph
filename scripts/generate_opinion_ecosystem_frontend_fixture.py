from __future__ import annotations

import argparse
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


def package_summary(manifest: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    data_scope = manifest.get("data_scope") if isinstance(manifest.get("data_scope"), dict) else {}
    return {
        "case_id": manifest.get("case_id", ""),
        "case_title": manifest.get("case_title", ""),
        "label": "Helldivers 2 / PSN small public sample",
        "evidence_items": int(data_scope.get("evidence_items_count") or len(evidence)),
        "sources": int(data_scope.get("source_urls_count") or len({item.get("source_url") for item in evidence if item.get("source_url")})),
        "comment_samples": int(data_scope.get("comment_sample_count") or sum(1 for item in evidence if item.get("evidence_type") in {"comment", "reply"})),
        "root_candidates": int(data_scope.get("root_content_count") or sum(1 for item in evidence if item.get("is_root_content"))),
        "validation_status": "passed_with_expected_warnings",
        "validation_warnings": [
            "one skipped Polygon source",
            "sample size below target",
        ],
        "coverage_notes": [
            "selected public sample only",
            "not full-web coverage",
            "not full-platform coverage",
            "not full-thread coverage",
            "not official verification",
            "not causal proof",
            "not production data",
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


def generate_fixture(package_dir: str | Path, out_file: str | Path) -> dict[str, Any]:
    package_path = Path(package_dir)
    output_path = Path(out_file)
    manifest = read_json(package_path / "manifest.json")
    evidence = [normalize_evidence_row(row) for row in read_jsonl(package_path / "evidence_items.jsonl")]
    summary = package_summary(manifest, evidence)
    public_manifest = {
        "case_id": manifest.get("case_id", ""),
        "case_title": manifest.get("case_title", ""),
        "package_version": manifest.get("package_version", ""),
        "contract_version": manifest.get("contract_version", ""),
        "exported_at": manifest.get("exported_at", ""),
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
                js_export("helldivers2PsnSampleManifest", public_manifest),
                js_export("helldivers2PsnEvidenceItems", evidence),
                js_export("helldivers2PsnSampleSummary", summary),
            ]
        ),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a frontend-local Opinion Ecosystem fixture from a Sentigraph Evidence Export v1 package.")
    parser.add_argument("--package", required=True, help="Local Evidence Export v1 package folder.")
    parser.add_argument("--out", required=True, help="Output frontend fixture module path.")
    args = parser.parse_args()
    summary = generate_fixture(args.package, args.out)
    print(
        "Generated frontend fixture: "
        f"evidence={summary['evidence_items']}, sources={summary['sources']}, comments={summary['comment_samples']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
