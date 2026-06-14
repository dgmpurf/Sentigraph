from __future__ import annotations

import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATOR_PATH = REPO_ROOT / "scripts" / "generate_opinion_ecosystem_frontend_fixture.py"
SAMPLE_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "samples"
    / "helldivers2_psn_demo"
    / "helldivers2-psn-demo_20260614_055754"
)


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_opinion_ecosystem_frontend_fixture", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generator_writes_frontend_fixture_from_helldivers_package(tmp_path: Path) -> None:
    generator = load_generator()
    out_file = tmp_path / "helldivers2PsnEvidenceFixture.js"

    summary = generator.generate_fixture(SAMPLE_PACKAGE, out_file)

    output = out_file.read_text(encoding="utf-8")
    assert summary["evidence_items"] == 34
    assert summary["sources"] == 7
    assert summary["comment_samples"] == 28
    assert "export const helldivers2PsnSampleManifest" in output
    assert "export const helldivers2PsnEvidenceItems" in output
    assert "export const helldivers2PsnSampleSummary" in output
    assert "Helldivers 2 PSN account linking controversy" in output
    assert "selected public sample only" in output.lower()
    assert "raw_author_id" not in output
    assert "raw_author_name" not in output
    assert "author_name" not in output
    assert "profile_url" not in output


def test_generator_strips_raw_identity_fields_from_tiny_package(tmp_path: Path) -> None:
    generator = load_generator()
    package_dir = tmp_path / "package"
    package_dir.mkdir()
    (package_dir / "manifest.json").write_text(
        json.dumps(
            {
                "case_id": "tiny_case",
                "case_title": "Tiny local package",
                "data_scope": {
                    "evidence_items_count": 1,
                    "source_urls_count": 1,
                    "comment_sample_count": 1,
                    "root_content_count": 0,
                },
                "coverage_note": "Selected public sample only; not full-web coverage; not full-platform coverage; not full-thread coverage; not official verification; not causal proof.",
            }
        ),
        encoding="utf-8",
    )
    row = {
        "evidence_id": "ev_1",
        "case_id": "tiny_case",
        "platform": "local",
        "source_type": "comment_sample",
        "acquisition_mode": "user_upload",
        "provenance_type": "external_agent_assisted",
        "verification_status": "source_url_provided_unverified",
        "trust_label": "medium_low",
        "trust_score": 0.45,
        "review_status": "review_needed",
        "evidence_type": "comment",
        "title": "",
        "body_text": "",
        "comment_text": "Short sample comment.",
        "language": "en",
        "source_url": "https://example.invalid/source",
        "url": "https://example.invalid/source",
        "root_id": "root_1",
        "parent_id": "",
        "created_at": "",
        "collected_at": "",
        "like_count": 0,
        "reply_count": 0,
        "share_count": 0,
        "view_count": 0,
        "content_hash": "hash_1",
        "normalized_content_hash": "hash_1",
        "canonical_url_hash": "url_hash_1",
        "duplicate_group_id": "dup_1",
        "duplicate_count": 1,
        "risk_flags": [],
        "content_visibility": "public",
        "access_scope": "public",
        "source_capture_method": "manual_comment_sample",
        "coverage_note": "Selected public sample only.",
        "raw_data_safe": {},
        "ingestion_metadata": {},
        "is_root_content": False,
        "comment_user_name": "raw name must not leak",
        "author_name": "raw name must not leak",
        "author_id": "raw id must not leak",
        "profile_url": "https://example.invalid/profile/raw",
    }
    (package_dir / "evidence_items.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    out_file = tmp_path / "fixture.js"

    generator.generate_fixture(package_dir, out_file)

    output = out_file.read_text(encoding="utf-8")
    assert "raw name must not leak" not in output
    assert "raw id must not leak" not in output
    assert "profile/raw" not in output
    assert "comment_user_name" not in output
    assert "author_name" not in output
    assert "author_id" not in output
    assert "profile_url" not in output
