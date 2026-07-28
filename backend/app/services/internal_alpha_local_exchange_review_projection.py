from __future__ import annotations

import os
import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final

from app.services.local_exchange_review_only_projection_bridge import (
    PROJECTION_FIELDS,
    build_disabled_local_exchange_review_only_projection,
    build_local_exchange_review_only_projection,
)
from app.services.local_exchange_review_only_staging_bridge import (
    LocalExchangeReviewOnlyStagingBridgeConfig,
    build_local_exchange_review_only_staging_response,
)


REGISTRY_SCHEMA: Final = "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1"
ROUTE_MODE: Final = "internal_alpha_read_only_local_exchange_projection_operator"
CAPABILITY_LABEL: Final = "b05_local_exchange_projection_read_only"
B05_GATE_ENV: Final = "SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED"
SAFE_SAMPLE_HANDLE_MAX_LENGTH: Final = 64
SAFE_SAMPLE_HANDLE_PATTERN: Final = r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$"

SHARED_ALPHA_GATE_ENV: Final = "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED"
B01_ROUTE_GATE_ENV: Final = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
B01_LOCAL_EXCHANGE_GATE_ENV: Final = (
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED"
)
B03_PROJECTION_GATE_ENV: Final = (
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED"
)
RESULTS_DIR_ENV: Final = "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"
EXPORT_ROOT_ENV: Final = "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"
ADAPTER_ID_ENV: Final = "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"

_SAFE_SAMPLE_HANDLE = re.compile(SAFE_SAMPLE_HANDLE_PATTERN)
_SAFE_RESULT_BASENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.json$")
_SAFE_ADAPTER_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_TRUE_VALUES = frozenset({"1", "true", "yes"})
_REQUIRED_GATES = (
    SHARED_ALPHA_GATE_ENV,
    B05_GATE_ENV,
    B01_ROUTE_GATE_ENV,
    B01_LOCAL_EXCHANGE_GATE_ENV,
    B03_PROJECTION_GATE_ENV,
)
_SAFE_DISPLAY_LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9 -]{0,78}[A-Za-z0-9])?$")
_SAFE_SAMPLE_ROLE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")

StagingBuilder = Callable[
    [str, LocalExchangeReviewOnlyStagingBridgeConfig],
    dict[str, Any],
]
ProjectionBuilder = Callable[[str, Mapping[str, Any] | object], dict[str, Any]]


@dataclass(frozen=True, slots=True)
class InternalAlphaLocalExchangeSampleRegistryEntry:
    sample_handle: str
    result_file_name: str
    display_label: str
    sample_role: str
    is_default: bool
    enabled: bool
    catalog_order: int
    route_mode: str
    capability_label: str


def validate_internal_alpha_local_exchange_sample_handle(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= SAFE_SAMPLE_HANDLE_MAX_LENGTH
        and _SAFE_SAMPLE_HANDLE.fullmatch(value) is not None
    )


def build_internal_alpha_local_exchange_sample_registry(
    entries: Iterable[InternalAlphaLocalExchangeSampleRegistryEntry] = (),
) -> MappingProxyType[str, InternalAlphaLocalExchangeSampleRegistryEntry]:
    registry: dict[str, InternalAlphaLocalExchangeSampleRegistryEntry] = {}
    for entry in entries:
        if not _is_bounded_registry_entry(entry):
            raise ValueError("invalid_registry_entry")
        if entry.sample_handle in registry:
            raise ValueError("duplicate_sample_handle")
        registry[entry.sample_handle] = entry
    return MappingProxyType(registry)


def build_internal_alpha_local_exchange_review_projection(
    sample_handle: object,
    *,
    registry: Mapping[str, InternalAlphaLocalExchangeSampleRegistryEntry] | None = None,
    environment: Mapping[str, str] | None = None,
    staging_builder: StagingBuilder | None = None,
    projection_builder: ProjectionBuilder | None = None,
) -> dict[str, Any]:
    if not validate_internal_alpha_local_exchange_sample_handle(sample_handle):
        return _disabled_projection("invalid_sample_handle")

    active_environment: Mapping[str, str] = os.environ if environment is None else environment
    if any(not _environment_gate_enabled(active_environment, gate) for gate in _REQUIRED_GATES):
        return _disabled_projection("b05_operator_surface_disabled")

    active_registry = DEFAULT_SAMPLE_REGISTRY if registry is None else registry
    entry = active_registry.get(sample_handle)
    if not isinstance(entry, InternalAlphaLocalExchangeSampleRegistryEntry) or not entry.enabled:
        return _disabled_projection("unknown_sample_handle")
    if entry.route_mode != ROUTE_MODE or entry.capability_label != CAPABILITY_LABEL:
        return _disabled_projection("registry_route_mismatch")

    config = _build_server_owned_configuration(active_environment)
    if config is None:
        return _disabled_projection("invalid_server_owned_configuration")

    active_staging_builder = staging_builder or build_local_exchange_review_only_staging_response
    upstream_response = active_staging_builder(entry.result_file_name, config)
    active_projection_builder = projection_builder or build_local_exchange_review_only_projection
    projection = active_projection_builder(entry.result_file_name, upstream_response)
    if tuple(projection) != PROJECTION_FIELDS or len(projection) != 52:
        return _disabled_projection("b05_projection_contract_mismatch")
    return projection


def _disabled_projection(error_code: str) -> dict[str, Any]:
    return build_disabled_local_exchange_review_only_projection(
        error_code,
        result_file_name=None,
    )


def _environment_gate_enabled(environment: Mapping[str, str], gate: str) -> bool:
    value = environment.get(gate)
    return isinstance(value, str) and value.strip().lower() in _TRUE_VALUES


def _build_server_owned_configuration(
    environment: Mapping[str, str],
) -> LocalExchangeReviewOnlyStagingBridgeConfig | None:
    results_dir = environment.get(RESULTS_DIR_ENV)
    export_root = environment.get(EXPORT_ROOT_ENV)
    adapter_id = environment.get(ADAPTER_ID_ENV)
    if not _is_bounded_server_value(results_dir, maximum=2_048):
        return None
    if not _is_bounded_server_value(export_root, maximum=2_048):
        return None
    if not isinstance(adapter_id, str) or _SAFE_ADAPTER_ID.fullmatch(adapter_id) is None:
        return None
    return LocalExchangeReviewOnlyStagingBridgeConfig(
        results_dir=results_dir,
        export_root=export_root,
        adapter_id=adapter_id,
    )


def _is_bounded_server_value(value: object, *, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and value == value.strip()
        and 0 < len(value) <= maximum
        and value.isprintable()
        and "\x00" not in value
    )


def _is_bounded_registry_entry(value: object) -> bool:
    return (
        isinstance(value, InternalAlphaLocalExchangeSampleRegistryEntry)
        and validate_internal_alpha_local_exchange_sample_handle(value.sample_handle)
        and isinstance(value.result_file_name, str)
        and 0 < len(value.result_file_name) <= 160
        and _SAFE_RESULT_BASENAME.fullmatch(value.result_file_name) is not None
        and isinstance(value.display_label, str)
        and _SAFE_DISPLAY_LABEL.fullmatch(value.display_label) is not None
        and isinstance(value.sample_role, str)
        and _SAFE_SAMPLE_ROLE.fullmatch(value.sample_role) is not None
        and isinstance(value.is_default, bool)
        and isinstance(value.enabled, bool)
        and isinstance(value.catalog_order, int)
        and not isinstance(value.catalog_order, bool)
        and 0 <= value.catalog_order <= 31
        and _is_bounded_label(value.route_mode)
        and _is_bounded_label(value.capability_label)
    )


def _is_bounded_label(value: object) -> bool:
    return (
        isinstance(value, str)
        and value == value.strip()
        and 0 < len(value) <= 160
        and value.isprintable()
    )


DEFAULT_SAMPLE_REGISTRY: Final = build_internal_alpha_local_exchange_sample_registry(
    (
        InternalAlphaLocalExchangeSampleRegistryEntry(
            sample_handle="helldivers2-psn-demo",
            result_file_name="provider_result_helldivers2-psn-demo_20260720_123627.json",
            display_label="Current curated sample",
            sample_role="current_curated",
            is_default=True,
            enabled=True,
            catalog_order=0,
            route_mode=ROUTE_MODE,
            capability_label=CAPABILITY_LABEL,
        ),
        InternalAlphaLocalExchangeSampleRegistryEntry(
            sample_handle="helldivers2-psn-demo-20260614",
            result_file_name="provider_result_helldivers2-psn-demo_20260614_055754.json",
            display_label="Accepted historical sample",
            sample_role="accepted_historical",
            is_default=False,
            enabled=True,
            catalog_order=1,
            route_mode=ROUTE_MODE,
            capability_label=CAPABILITY_LABEL,
        ),
    )
)
