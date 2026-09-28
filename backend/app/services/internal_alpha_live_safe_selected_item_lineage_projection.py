"""Detached, bounded selected-item lineage contract for the internal live-safe route."""

from __future__ import annotations

from collections.abc import Mapping
import re
from types import MappingProxyType


SOURCE_FIELDS = (
    "review_binding_mode",
    "reviewed_batch_safe_hash",
    "fresh_batch_safe_hash",
    "selected_discussion_safe_hash",
    "reply_content_acquired",
    "author_identity_omitted",
)
PROJECTION_SCHEMA = "sentigraph_internal_alpha_live_safe_selected_item_lineage_projection_v0_1"
PROJECTION_MODE = "persisted_exact_one_safe_attestation_only"
CONTRACT_ERROR = "live_safe_selected_item_lineage_contract_mismatch"
_SAFE_HASH = re.compile(r"[0-9a-f]{64}")
_SELECTOR = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.:-]{0,255}")


class LiveSafeLineageUnavailable(LookupError):
    """The exact bound selector has no available persisted item."""


class LiveSafeLineageAmbiguous(LookupError):
    """The exact bound selector matches more than one persisted item."""


class LiveSafeLineageContractError(ValueError):
    """Persisted safe attestations are malformed or violate the privacy contract."""


def validate_live_safe_selector(case_id: str, evidence_id: str) -> None:
    """Reject malformed path selectors before a store or provider can be reached."""
    if any(type(value) is not str or _SELECTOR.fullmatch(value) is None for value in (case_id, evidence_id)):
        raise LiveSafeLineageContractError(CONTRACT_ERROR)


def validate_live_safe_source(source: Mapping[str, object]) -> Mapping[str, str | bool]:
    """Accept only the six detached producer attestations, never a full evidence row."""
    if type(source) not in (dict, MappingProxyType) or set(source) != set(SOURCE_FIELDS):
        raise LiveSafeLineageContractError(CONTRACT_ERROR)
    if type(source["review_binding_mode"]) is not str or source["review_binding_mode"] != "selected_item_v1":
        raise LiveSafeLineageContractError(CONTRACT_ERROR)
    for field in SOURCE_FIELDS[1:4]:
        value = source[field]
        if type(value) is not str or _SAFE_HASH.fullmatch(value) is None:
            raise LiveSafeLineageContractError(CONTRACT_ERROR)
    if source["reply_content_acquired"] is not False or source["author_identity_omitted"] is not True:
        raise LiveSafeLineageContractError(CONTRACT_ERROR)
    return MappingProxyType({field: source[field] for field in SOURCE_FIELDS})


def build_live_safe_selected_item_lineage_projection(
    source: Mapping[str, object],
) -> Mapping[str, str | bool]:
    """Project already detached scalars without upgrading provenance into trust."""
    safe = validate_live_safe_source(source)
    return MappingProxyType({
        "projection_schema": PROJECTION_SCHEMA,
        "projection_mode": PROJECTION_MODE,
        "binding_mode": safe["review_binding_mode"],
        "reviewed_batch_safe_hash": safe["reviewed_batch_safe_hash"],
        "fresh_batch_safe_hash": safe["fresh_batch_safe_hash"],
        "persisted_selected_safe_hash": safe["selected_discussion_safe_hash"],
        "selected_binding_evidence_present": True,
        "reply_content_acquired": False,
        "author_identity_omitted_at_production": True,
        "transport_source_provenance_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "synthetic_fixture_only": False,
        "live_persisted_record_connected": True,
    })
