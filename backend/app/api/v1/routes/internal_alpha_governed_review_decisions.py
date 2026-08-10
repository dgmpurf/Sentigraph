from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, StrictStr

from app.services.governed_nonproduction_human_review_decision_ledger import (
    FORMAL_STATE_DISABLED,
    FORMAL_STATE_INCONSISTENT,
    FORMAL_STATE_READY,
    FORMAL_STATE_UNAVAILABLE,
    FORMAL_STATE_UNAVAILABLE_ERROR,
    GovernedNonproductionHumanReviewDecisionIntegrityError,
    GovernedNonproductionHumanReviewDecisionLedger,
    GovernedNonproductionHumanReviewDecisionLedgerUnavailable,
    _formal_state_projection,
    get_governed_nonproduction_human_review_decision,
    project_exact_formal_governed_nonproduction_human_review_decision_state,
    record_second_exact_formal_human_review_decision,
    record_governed_nonproduction_human_review_decision,
    validate_second_exact_formal_human_review_decision_activation,
)


GATE = "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_LEDGER_ENABLED"
FORMAL_SECOND_GATE = (
    "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_FORMAL_SECOND_ENABLED"
)
FORMAL_STATE_PROJECTION_GATE = (
    "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_"
    "FORMAL_STATE_PROJECTION_ENABLED"
)
FORMAL_SECOND_ACTIVATION_JSON = (
    "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_"
    "FORMAL_SECOND_ACTIVATION_JSON"
)
FORMAL_SECOND_ACTIVATION_SHA256 = (
    "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_"
    "FORMAL_SECOND_ACTIVATION_SHA256"
)
ROUTE_MODE = (
    "internal_disabled_by_default_append_only_nonproduction_"
    "human_review_decision_ledger"
)
POST_RESPONSE_SCHEMA = (
    "sentigraph_internal_alpha_governed_review_decision_post_response_v0_1"
)
GET_RESPONSE_SCHEMA = (
    "sentigraph_internal_alpha_governed_review_decision_get_response_v0_1"
)
OUTCOME_STATUS = {
    "created_exactly_one_human_review_decision": 201,
    "already_exists_same_human_review_decision": 200,
    "blocked_unsupported_decision_type": 422,
    "blocked_binding_or_snapshot_mismatch": 409,
    "blocked_idempotency_conflict": 409,
    "paused_pending_read_only_idempotency_verification": 503,
    "bounded_decision_ledger_failure": 500,
}
FORMAL_STATE_STATUS_CODE = {
    FORMAL_STATE_READY: 200,
    FORMAL_STATE_DISABLED: 404,
    FORMAL_STATE_INCONSISTENT: 409,
    FORMAL_STATE_UNAVAILABLE: 503,
}

router = APIRouter()
_formal_second_activation_consumed = False


class GovernedNonproductionHumanReviewDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    request_schema: StrictStr
    request_version: StrictStr
    decision_type: StrictStr


def _ledger_factory() -> GovernedNonproductionHumanReviewDecisionLedger:
    return GovernedNonproductionHumanReviewDecisionLedger()


def _gate_enabled() -> bool:
    return os.getenv(GATE, "").strip().lower() in {"1", "true", "yes", "on"}


def _formal_second_gate_enabled() -> bool:
    return os.getenv(FORMAL_SECOND_GATE, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _formal_state_projection_gate_enabled() -> bool:
    return os.getenv(FORMAL_STATE_PROJECTION_GATE, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _strict_json_object(value: str) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        keys = [key for key, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate_json_key")
        return dict(pairs)

    def reject_constant(_value: str) -> None:
        raise ValueError("nonstandard_json_constant")

    parsed = json.loads(
        value,
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    if not isinstance(parsed, dict):
        raise ValueError("activation_not_object")
    return parsed


def _formal_second_activation() -> tuple[dict[str, Any], str] | None:
    raw = os.getenv(FORMAL_SECOND_ACTIVATION_JSON)
    safe_hash = os.getenv(FORMAL_SECOND_ACTIVATION_SHA256)
    if raw is None or safe_hash is None:
        return None
    try:
        activation = _strict_json_object(raw)
        validated = (
            validate_second_exact_formal_human_review_decision_activation(
                activation,
                safe_hash,
            )
        )
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    except GovernedNonproductionHumanReviewDecisionIntegrityError:
        return None
    return validated, safe_hash


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _post_response(
    *,
    decision: dict[str, Any] | None,
    receipt: dict[str, Any] | None,
) -> dict[str, Any]:
    decision_id = decision.get("decision_id") if decision is not None else None
    if decision_id is None and receipt is not None:
        decision_id = receipt.get("decision_id")
    write_performed = bool(
        receipt is not None
        and receipt.get("outcome")
        == "created_exactly_one_human_review_decision"
        and receipt.get("mutation_count") == 1
    )
    return {
        "response_schema": POST_RESPONSE_SCHEMA,
        "route_mode": ROUTE_MODE,
        "decision_id": decision_id,
        "decision": decision,
        "receipt": receipt,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "decision_ledger_write_performed": write_performed,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "operator_runtime_ready": False,
        "public_ready": False,
        "production_ready": False,
    }


def _get_response(
    *,
    decision_id: str,
    decision: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "response_schema": GET_RESPONSE_SCHEMA,
        "route_mode": ROUTE_MODE,
        "decision_id": decision_id,
        "decision": decision,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "operator_runtime_ready": False,
        "public_ready": False,
        "production_ready": False,
    }


@router.post("/decisions")
def post_decision(
    request: GovernedNonproductionHumanReviewDecisionRequest,
) -> JSONResponse:
    if not _gate_enabled():
        return JSONResponse(
            status_code=404,
            content=_post_response(
                decision=None,
                receipt=None,
            ),
        )
    if _formal_second_gate_enabled():
        global _formal_second_activation_consumed
        activation = _formal_second_activation()
        if activation is None or _formal_second_activation_consumed:
            return JSONResponse(
                status_code=503,
                content=_post_response(
                    decision=None,
                    receipt=None,
                ),
            )
        activation_object, activation_hash = activation
        _formal_second_activation_consumed = True
        try:
            result = record_second_exact_formal_human_review_decision(
                repository_root=_repository_root(),
                request=request.model_dump(),
                second_activation_object=activation_object,
                second_activation_binding_safe_hash=activation_hash,
                enabled=True,
            )
        except Exception:
            return JSONResponse(
                status_code=503,
                content=_post_response(
                    decision=None,
                    receipt=None,
                ),
            )
        decision = result.get("decision")
        receipt = result.get("receipt")
        if not isinstance(receipt, dict):
            return JSONResponse(
                status_code=503,
                content=_post_response(
                    decision=None,
                    receipt=None,
                ),
            )
        outcome = receipt.get("outcome")
        status_code = OUTCOME_STATUS.get(outcome, 503)
        return JSONResponse(
            status_code=status_code,
            content=_post_response(
                decision=decision if isinstance(decision, dict) else None,
                receipt=receipt,
            ),
        )
    ledger = _ledger_factory()
    if not ledger.enabled or ledger.database_path is None:
        return JSONResponse(
            status_code=503,
            content=_post_response(
                decision=None,
                receipt=None,
            ),
        )
    decision, receipt = record_governed_nonproduction_human_review_decision(
        ledger,
        request.model_dump(),
    )
    outcome = receipt["outcome"]
    return JSONResponse(
        status_code=OUTCOME_STATUS[outcome],
        content=_post_response(
            decision=decision,
            receipt=receipt,
        ),
    )


@router.get("/formal-state")
def get_formal_state() -> JSONResponse:
    try:
        projection = (
            project_exact_formal_governed_nonproduction_human_review_decision_state(
                repository_root=_repository_root(),
                enabled=(
                    _gate_enabled()
                    and _formal_state_projection_gate_enabled()
                ),
            )
        )
    except Exception:
        projection = _formal_state_projection(
            FORMAL_STATE_UNAVAILABLE,
            FORMAL_STATE_UNAVAILABLE_ERROR,
        )
    return JSONResponse(
        status_code=FORMAL_STATE_STATUS_CODE.get(
            projection.get("projection_status"),
            503,
        ),
        content=projection,
    )


@router.get("/decisions/{decision_id}")
def get_decision(decision_id: str) -> JSONResponse:
    if re.fullmatch(r"ghrd-[0-9a-f]{32}", decision_id) is None:
        return JSONResponse(
            status_code=422,
            content=_get_response(
                decision_id=decision_id,
                decision=None,
            ),
        )
    if not _gate_enabled():
        return JSONResponse(
            status_code=404,
            content=_get_response(
                decision_id=decision_id,
                decision=None,
            ),
        )
    ledger = _ledger_factory()
    if not ledger.enabled or ledger.database_path is None:
        return JSONResponse(
            status_code=503,
            content=_get_response(
                decision_id=decision_id,
                decision=None,
            ),
        )
    try:
        decision = get_governed_nonproduction_human_review_decision(
            ledger,
            decision_id,
        )
    except GovernedNonproductionHumanReviewDecisionIntegrityError:
        return JSONResponse(
            status_code=409,
            content=_get_response(
                decision_id=decision_id,
                decision=None,
            ),
        )
    except GovernedNonproductionHumanReviewDecisionLedgerUnavailable:
        return JSONResponse(
            status_code=503,
            content=_get_response(
                decision_id=decision_id,
                decision=None,
            ),
        )
    return JSONResponse(
        status_code=200 if decision is not None else 404,
        content=_get_response(
            decision_id=decision_id,
            decision=decision,
        ),
    )
