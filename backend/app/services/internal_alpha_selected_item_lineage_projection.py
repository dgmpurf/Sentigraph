"""Pure, synthetic-only projection of selected-item producer attestations."""

from __future__ import annotations

from collections.abc import Mapping
import re
from types import MappingProxyType


PROJECTION_SCHEMA = "sentigraph_internal_alpha_selected_item_lineage_projection_v0_1"
PROJECTION_MODE = "producer_attestation_synthetic_fixture_only"
SOURCE_FIELDS = (
    "review_binding_mode",
    "reviewed_batch_safe_hash",
    "fresh_batch_safe_hash",
    "selected_discussion_safe_hash",
    "reply_content_acquired",
    "author_identity_omitted",
)
PROJECTION_FIELDS = (
    "projection_schema",
    "projection_mode",
    "binding_mode",
    "reviewed_batch_safe_hash",
    "fresh_batch_safe_hash",
    "persisted_selected_safe_hash",
    "selected_binding_evidence_present",
    "reply_content_acquired",
    "author_identity_omitted_at_production",
    "transport_source_provenance_only",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "synthetic_fixture_only",
    "live_persisted_record_connected",
)
CONTRACT_ERROR = "selected_item_lineage_source_contract_mismatch"
_SAFE_HASH = re.compile(r"[0-9a-f]{64}")


def build_internal_alpha_selected_item_lineage_projection(
    source: Mapping[str, object],
) -> Mapping[str, str | bool]:
    """Validate six safe scalars and return a detached immutable attestation.

    This accepts no full case, evidence, job or provider object. A persisted
    digest remains one digest; it is not a new independent equality check.
    No I/O or mutation occurs, and missing facts never become default values.
    """
    if type(source) not in (dict, MappingProxyType) or set(source) != set(SOURCE_FIELDS):
        raise ValueError(CONTRACT_ERROR)
    if type(source["review_binding_mode"]) is not str or source["review_binding_mode"] != "selected_item_v1":
        raise ValueError(CONTRACT_ERROR)
    for field in SOURCE_FIELDS[1:4]:
        value = source[field]
        if type(value) is not str or _SAFE_HASH.fullmatch(value) is None:
            raise ValueError(CONTRACT_ERROR)
    for field in SOURCE_FIELDS[4:]:
        if type(source[field]) is not bool:
            raise ValueError(CONTRACT_ERROR)

    return MappingProxyType({
        "projection_schema": PROJECTION_SCHEMA,
        "projection_mode": PROJECTION_MODE,
        "binding_mode": "selected_item_v1",
        "reviewed_batch_safe_hash": source["reviewed_batch_safe_hash"],
        "fresh_batch_safe_hash": source["fresh_batch_safe_hash"],
        "persisted_selected_safe_hash": source["selected_discussion_safe_hash"],
        "selected_binding_evidence_present": True,
        "reply_content_acquired": source["reply_content_acquired"],
        "author_identity_omitted_at_production": source["author_identity_omitted"],
        "transport_source_provenance_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "synthetic_fixture_only": True,
        "live_persisted_record_connected": False,
    })
