from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any, Final

from app.services.internal_alpha_local_exchange_review_projection import (
    CAPABILITY_LABEL,
    DEFAULT_SAMPLE_REGISTRY,
    ROUTE_MODE,
    InternalAlphaLocalExchangeSampleRegistryEntry,
    validate_internal_alpha_local_exchange_sample_handle,
)


CATALOG_SCHEMA: Final = "sentigraph_internal_alpha_local_exchange_sample_catalog_v0_1"
CATALOG_VERSION: Final = "0.1"
CATALOG_MODE: Final = "internal_alpha_read_only_local_exchange_sample_catalog"
CATALOG_FIELDS: Final = (
    "schema",
    "version",
    "mode",
    "status",
    "sample_count",
    "default_sample_handle",
    "samples",
    "read_only",
    "human_review_required",
    "production_ready",
    "mutable_authority_granted",
)
SAMPLE_FIELDS: Final = (
    "sample_handle",
    "display_label",
    "sample_role",
    "is_default",
    "enabled",
    "catalog_order",
)
MAX_CATALOG_SAMPLES: Final = 32

_SAFE_DISPLAY_LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9 -]{0,78}[A-Za-z0-9])?$")
_SAFE_SAMPLE_ROLE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


def build_internal_alpha_local_exchange_sample_catalog(
    registry: Mapping[str, InternalAlphaLocalExchangeSampleRegistryEntry] | None = None,
) -> dict[str, Any]:
    active_registry = DEFAULT_SAMPLE_REGISTRY if registry is None else registry
    entries = tuple(active_registry.values()) if isinstance(active_registry, Mapping) else ()
    if not _is_valid_catalog_registry(active_registry, entries):
        raise ValueError("invalid_sample_catalog")

    default_entry = next(entry for entry in entries if entry.is_default)
    samples = [
        {
            "sample_handle": entry.sample_handle,
            "display_label": entry.display_label,
            "sample_role": entry.sample_role,
            "is_default": entry.is_default,
            "enabled": entry.enabled,
            "catalog_order": entry.catalog_order,
        }
        for entry in entries
    ]
    return {
        "schema": CATALOG_SCHEMA,
        "version": CATALOG_VERSION,
        "mode": CATALOG_MODE,
        "status": "ready",
        "sample_count": len(samples),
        "default_sample_handle": default_entry.sample_handle,
        "samples": samples,
        "read_only": True,
        "human_review_required": True,
        "production_ready": False,
        "mutable_authority_granted": False,
    }


def build_unavailable_internal_alpha_local_exchange_sample_catalog() -> dict[str, Any]:
    return {
        "schema": CATALOG_SCHEMA,
        "version": CATALOG_VERSION,
        "mode": CATALOG_MODE,
        "status": "unavailable",
        "sample_count": 0,
        "default_sample_handle": None,
        "samples": [],
        "read_only": True,
        "human_review_required": True,
        "production_ready": False,
        "mutable_authority_granted": False,
    }


def _is_valid_catalog_registry(
    registry: object,
    entries: tuple[object, ...],
) -> bool:
    if not isinstance(registry, Mapping) or not 0 < len(entries) <= MAX_CATALOG_SAMPLES:
        return False
    if not all(isinstance(entry, InternalAlphaLocalExchangeSampleRegistryEntry) for entry in entries):
        return False

    typed_entries = tuple(entry for entry in entries if isinstance(entry, InternalAlphaLocalExchangeSampleRegistryEntry))
    handles = tuple(entry.sample_handle for entry in typed_entries)
    labels = tuple(entry.display_label for entry in typed_entries)
    if tuple(registry.keys()) != handles or len(set(handles)) != len(handles):
        return False
    if len(set(labels)) != len(labels):
        return False
    if tuple(entry.catalog_order for entry in typed_entries) != tuple(range(len(typed_entries))):
        return False

    defaults = tuple(entry for entry in typed_entries if entry.is_default)
    if len(defaults) != 1 or not defaults[0].enabled:
        return False

    return all(
        validate_internal_alpha_local_exchange_sample_handle(entry.sample_handle)
        and _SAFE_DISPLAY_LABEL.fullmatch(entry.display_label) is not None
        and _SAFE_SAMPLE_ROLE.fullmatch(entry.sample_role) is not None
        and isinstance(entry.is_default, bool)
        and isinstance(entry.enabled, bool)
        and isinstance(entry.catalog_order, int)
        and not isinstance(entry.catalog_order, bool)
        and entry.route_mode == ROUTE_MODE
        and entry.capability_label == CAPABILITY_LABEL
        for entry in typed_entries
    )
