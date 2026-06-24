from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


LocalExchangeReadStatus = Literal[
    "disabled",
    "metadata_ready",
    "blocked",
    "invalid_schema",
    "unsupported_contract",
    "manual_review_required",
    "not_found",
    "failed",
]


class LocalExchangeReaderConfig(BaseModel):
    exchange_enabled: bool = False
    requestsDir: str = ""
    resultsDir: str = ""
    packageIndexPath: str = ""
    packageRoot: str = ""
    exchangeLogPath: str = ""
    request_schema: str = "sentigraph_analysis_request_v1"
    result_schema: str = "sentigraph_provider_job_result_v1"
    contract_version: str = "1.0"
    adapter_id: str = ""


class LocalExchangeProviderResultMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    result_schema: str = "sentigraph_provider_job_result_v1"
    request_schema: str | None = None
    contract_version: str = "1.0"
    adapter_id: str = ""
    compatibility_status: str = "compatible"
    status: str = ""
    provider_result_id: str = ""
    provider_job_id: str = ""
    sentigraph_request_id: str = ""
    package_contract: str = ""
    package_id: str = ""
    package_role: str = ""
    package_index_ref: str = ""
    package_root_ref: str = ""
    package_relative_path: str = ""
    summary: dict[str, Any] = Field(default_factory=dict)
    validation_summary: dict[str, Any] = Field(default_factory=dict)
    coverage_note: str = ""
    warnings: list[Any] = Field(default_factory=list)
    errors: list[Any] = Field(default_factory=list)
    nextAction: str = ""

    @model_validator(mode="before")
    @classmethod
    def normalize_schema_alias(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "result_schema" not in normalized and "schema" in normalized:
            normalized["result_schema"] = normalized.get("schema")
        return normalized


def local_exchange_safe_mode() -> dict[str, bool]:
    return {
        "metadata_only": True,
        "file_read_attempted": False,
        "package_index_read": False,
        "evidence_items_read": False,
        "evidence_items_parsed": False,
        "evidence_items_imported": False,
        "evidence_layer_written": False,
        "production_case_created": False,
        "production_review_queue_created": False,
        "production_dedup_run": False,
        "analysis_run_created": False,
        "b_end_report_generated": False,
        "sandbox_fixture_generated": False,
        "public_event_page_generated": False,
        "provider_execution": False,
        "collector_jobs_run": False,
        "http_provider_integration": False,
        "real_api_calls": False,
        "real_llm_calls": False,
        "url_fetching": False,
        "scraping": False,
        "secrets_exposed": False,
        "raw_author_identifiers_exposed": False,
        "public_download_route_created": False,
        "file_byte_response_created": False,
        "zip_generated": False,
        "public_url_generated": False,
        "signed_url_generated": False,
        "external_delivery_performed": False,
    }


class LocalExchangeReaderResult(BaseModel):
    status: LocalExchangeReadStatus
    metadata: LocalExchangeProviderResultMetadata | None = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    forbidden_fields: list[str] = Field(default_factory=list)
    file_read_attempted: bool = False
    result_file_exists: bool = False
    safe_mode: dict[str, bool] = Field(default_factory=local_exchange_safe_mode)
