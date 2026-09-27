from __future__ import annotations

import ast
from pathlib import Path
from types import MappingProxyType

import pytest

from app.services.internal_alpha_selected_item_lineage_projection import (
    CONTRACT_ERROR,
    PROJECTION_FIELDS,
    PROJECTION_MODE,
    PROJECTION_SCHEMA,
    SOURCE_FIELDS,
    build_internal_alpha_selected_item_lineage_projection,
)


def safe_source() -> dict[str, object]:
    return {
        "review_binding_mode": "selected_item_v1",
        "reviewed_batch_safe_hash": "1" * 64,
        "fresh_batch_safe_hash": "2" * 64,
        "selected_discussion_safe_hash": "3" * 64,
        "reply_content_acquired": False,
        "author_identity_omitted": True,
    }


def test_exact_detached_immutable_projection_and_policy() -> None:
    source = safe_source()
    before = dict(source)
    projection = build_internal_alpha_selected_item_lineage_projection(source)
    assert tuple(projection) == PROJECTION_FIELDS
    assert dict(projection) == {
        "projection_schema": PROJECTION_SCHEMA,
        "projection_mode": PROJECTION_MODE,
        "binding_mode": "selected_item_v1",
        "reviewed_batch_safe_hash": "1" * 64,
        "fresh_batch_safe_hash": "2" * 64,
        "persisted_selected_safe_hash": "3" * 64,
        "selected_binding_evidence_present": True,
        "reply_content_acquired": False,
        "author_identity_omitted_at_production": True,
        "transport_source_provenance_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "synthetic_fixture_only": True,
        "live_persisted_record_connected": False,
    }
    assert source == before
    source["selected_discussion_safe_hash"] = "4" * 64
    assert projection["persisted_selected_safe_hash"] == "3" * 64
    with pytest.raises(TypeError):
        projection["human_review_required"] = False  # type: ignore[index]


def test_immutable_safe_input_mapping_is_supported() -> None:
    assert build_internal_alpha_selected_item_lineage_projection(
        MappingProxyType(safe_source())
    )["selected_binding_evidence_present"] is True


@pytest.mark.parametrize("field", SOURCE_FIELDS[1:4])
@pytest.mark.parametrize("invalid", ["a" * 63, "a" * 65, "A" * 64, "g" * 64, "a" * 64 + "\n", 1, None])
def test_hashes_are_strict_lower_hex_64(field: str, invalid: object) -> None:
    source = safe_source()
    source[field] = invalid
    with pytest.raises(ValueError, match=f"^{CONTRACT_ERROR}$"):
        build_internal_alpha_selected_item_lineage_projection(source)


@pytest.mark.parametrize("invalid", ["batch_v1", "SELECTED_ITEM_V1", None, 1, True])
def test_wrong_binding_mode_is_rejected(invalid: object) -> None:
    source = safe_source()
    source["review_binding_mode"] = invalid
    with pytest.raises(ValueError, match=f"^{CONTRACT_ERROR}$"):
        build_internal_alpha_selected_item_lineage_projection(source)


@pytest.mark.parametrize("field", SOURCE_FIELDS)
def test_missing_source_field_never_becomes_a_default(field: str) -> None:
    source = safe_source()
    del source[field]
    with pytest.raises(ValueError, match=f"^{CONTRACT_ERROR}$"):
        build_internal_alpha_selected_item_lineage_projection(source)


@pytest.mark.parametrize("field", SOURCE_FIELDS[4:])
@pytest.mark.parametrize("invalid", [0, 1, "true", "false", None, {}, []])
def test_boolean_coercion_is_rejected(field: str, invalid: object) -> None:
    source = safe_source()
    source[field] = invalid
    with pytest.raises(ValueError, match=f"^{CONTRACT_ERROR}$"):
        build_internal_alpha_selected_item_lineage_projection(source)


@pytest.mark.parametrize("field", [
    "extra", "body_text", "discussion_id", "video_id", "comment_id", "author_id",
    "source_url", "case_id", "evidence_id", "job_id", "raw_provider_payload",
    "reviewed_selected_safe_hash", "fresh_selected_safe_hash",
    "selected_safe_lineage_consistent", "author_identity_absent",
])
def test_unknown_forbidden_and_blocked_keys_cannot_pass(field: str) -> None:
    source = safe_source()
    source[field] = "synthetic_forbidden_marker"
    with pytest.raises(ValueError, match=f"^{CONTRACT_ERROR}$"):
        build_internal_alpha_selected_item_lineage_projection(source)
    assert field not in build_internal_alpha_selected_item_lineage_projection(safe_source())


@pytest.mark.parametrize("invalid", [None, [], "raw_object", object()])
def test_full_objects_or_non_mapping_input_are_rejected(invalid: object) -> None:
    with pytest.raises(ValueError, match=f"^{CONTRACT_ERROR}$"):
        build_internal_alpha_selected_item_lineage_projection(invalid)  # type: ignore[arg-type]


def test_service_has_no_provider_store_environment_or_io_dependency() -> None:
    source_path = Path(__file__).parents[1] / "services/internal_alpha_selected_item_lineage_projection.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    imports = {
        node.module if isinstance(node, ast.ImportFrom) else alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert imports == {"__future__", "collections.abc", "re", "types"}
    forbidden = {"open", "getenv", "get_case", "get_case_repository", "save_case_evidence", "request", "fetch"}
    calls = {
        node.func.id if isinstance(node.func, ast.Name) else node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, (ast.Name, ast.Attribute))
    }
    assert calls.isdisjoint(forbidden)
