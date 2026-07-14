from __future__ import annotations

import os
import re
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, StrictStr

from app.services.governed_nonproduction_human_review_decision_ledger import (
    GovernedNonproductionHumanReviewDecisionIntegrityError,
    GovernedNonproductionHumanReviewDecisionLedger,
    GovernedNonproductionHumanReviewDecisionLedgerUnavailable,
    get_governed_nonproduction_human_review_decision,
    record_governed_nonproduction_human_review_decision,
)


GATE = "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_LEDGER_ENABLED"
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

router = APIRouter()


class GovernedNonproductionHumanReviewDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    request_schema: StrictStr
    request_version: StrictStr
    decision_type: StrictStr


def _ledger_factory() -> GovernedNonproductionHumanReviewDecisionLedger:
    return GovernedNonproductionHumanReviewDecisionLedger()


def _gate_enabled() -> bool:
    return os.getenv(GATE, "").strip().lower() in {"1", "true", "yes", "on"}


def _post_response(
    *,
    route_mode: str,
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
        "route_mode": route_mode,
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
    route_mode: str,
    decision_id: str,
    decision: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "response_schema": GET_RESPONSE_SCHEMA,
        "route_mode": route_mode,
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
                route_mode="disabled_internal_alpha",
                decision=None,
                receipt=None,
            ),
        )
    ledger = _ledger_factory()
    if not ledger.enabled or ledger.database_path is None:
        return JSONResponse(
            status_code=503,
            content=_post_response(
                route_mode="unavailable_synthetic_only",
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
            route_mode="synthetic_only_governed_nonproduction",
            decision=decision,
            receipt=receipt,
        ),
    )


@router.get("/decisions/{decision_id}")
def get_decision(decision_id: str) -> JSONResponse:
    if re.fullmatch(r"ghrd-[0-9a-f]{32}", decision_id) is None:
        return JSONResponse(
            status_code=422,
            content=_get_response(
                route_mode="request_rejected",
                decision_id=decision_id,
                decision=None,
            ),
        )
    if not _gate_enabled():
        return JSONResponse(
            status_code=404,
            content=_get_response(
                route_mode="disabled_internal_alpha",
                decision_id=decision_id,
                decision=None,
            ),
        )
    ledger = _ledger_factory()
    if not ledger.enabled or ledger.database_path is None:
        return JSONResponse(
            status_code=503,
            content=_get_response(
                route_mode="unavailable_synthetic_only",
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
                route_mode="integrity_blocked",
                decision_id=decision_id,
                decision=None,
            ),
        )
    except GovernedNonproductionHumanReviewDecisionLedgerUnavailable:
        return JSONResponse(
            status_code=503,
            content=_get_response(
                route_mode="unavailable_synthetic_only",
                decision_id=decision_id,
                decision=None,
            ),
        )
    return JSONResponse(
        status_code=200 if decision is not None else 404,
        content=_get_response(
            route_mode="synthetic_only_governed_nonproduction",
            decision_id=decision_id,
            decision=decision,
        ),
    )
