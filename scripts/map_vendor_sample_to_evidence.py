from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from typing import Any


SECRET_KEY_MARKERS = {
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "client_secret",
    "password",
    "cookie",
    "authorization",
    "token",
    "secret",
    ".env",
}

SECRET_TEXT_PATTERN = re.compile(
    r"\b(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|cookie|authorization)\b\s*[:=]\s*([^\s,;]+)",
    re.IGNORECASE,
)

FORMULA_PREFIXES = ("=", "+", "-", "@")

SOURCE_TYPE_VALUES = {
    "youtube",
    "douyin",
    "bilibili",
    "weibo",
    "xiaohongshu",
    "reddit",
    "news_site",
    "forum",
    "public_web",
    "uploaded_dataset",
    "mock",
}

KNOWN_PLATFORM_CLAIMS = {
    *SOURCE_TYPE_VALUES,
    "kuaishou",
    "zhihu",
    "douban",
    "toutiao",
    "the_paper",
    "jiemian",
    "hupu",
    "tieba",
    "nga",
    "maimai",
    "xueqiu",
    "eastmoney",
    "stocktwits",
    "tiktok",
    "x",
    "twitter",
    "bluesky",
    "mastodon",
}

EVIDENCE_TYPE_VALUES = {
    "video",
    "article",
    "post",
    "comment",
    "reply",
    "title",
    "body_text",
    "metadata",
    "interaction_metric",
    "search_result",
    "uploaded_record",
}

FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "source_provider": ("source_provider", "provider", "vendor", "vendor_name", "data_provider"),
    "platform": ("platform", "source_platform", "site", "channel"),
    "source_type": ("source_type", "source", "source_bucket", "source_category"),
    "acquisition_mode": ("acquisition_mode", "mode", "collection_mode"),
    "evidence_type": ("evidence_type", "content_type", "type", "record_type"),
    "query": ("query", "keyword", "event_query", "search_query"),
    "content_id": ("content_id", "id", "record_id", "post_id", "article_id", "video_id", "comment_id", "item_id"),
    "parent_id": ("parent_id", "parent_comment_id", "parent_content_id"),
    "root_id": ("root_id", "thread_id", "post_id", "article_id", "video_id", "item_id"),
    "url": ("url", "source_url", "link", "permalink"),
    "title": ("title", "headline", "article_title", "video_title", "post_title"),
    "body_text": ("body_text", "body", "content", "text", "description", "snippet", "summary"),
    "comment_text": ("comment_text", "comment", "reply_text", "comment_body", "message"),
    "author_id": ("author_id", "user_id", "uid", "author_uid", "account_id"),
    "author_name": ("author_name", "author", "nickname", "display_name", "user_name", "screen_name"),
    "created_at": ("created_at", "published_at", "timestamp", "time", "create_time", "post_time"),
    "collected_at": ("collected_at", "crawled_at", "fetched_at", "ingested_at", "collection_time"),
    "like_count": ("like_count", "likes", "like", "favorite_count"),
    "reply_count": ("reply_count", "replies", "comments", "comment_count"),
    "share_count": ("share_count", "shares", "share", "forward_count"),
    "view_count": ("view_count", "views", "view", "play_count"),
    "repost_count": ("repost_count", "reposts", "retweet_count", "repost"),
    "language": ("language", "lang", "locale"),
    "collection_method": ("collection_method", "source_route", "data_source_route"),
    "collection_basis": ("collection_basis", "legal_basis", "license_basis"),
    "source_terms_url": ("source_terms_url", "terms_url", "platform_terms_url"),
    "vendor_license_id": ("vendor_license_id", "license_id", "contract_id", "order_id"),
    "commercial_use_allowed": ("commercial_use_allowed", "commercial_allowed", "client_reports_allowed"),
    "storage_allowed": ("storage_allowed", "normalized_storage_allowed"),
    "retention_allowed_until": ("retention_allowed_until", "retention_until", "retention_policy"),
    "deletion_sync_supported": ("deletion_sync_supported", "takedown_sync_supported", "deletion_sync"),
    "personal_data_classification": ("personal_data_classification", "personal_data", "pii_classification"),
    "vendor_attestation": ("vendor_attestation", "vendor_attested", "lawful_source_attestation", "attestation"),
}

COMPLIANCE_FIELDS = {
    "collection_method",
    "collection_basis",
    "source_terms_url",
    "vendor_license_id",
    "commercial_use_allowed",
    "storage_allowed",
    "retention_allowed_until",
    "deletion_sync_supported",
    "personal_data_classification",
    "vendor_attestation",
}


@dataclass
class VendorMappingWarning:
    row_number: int | None
    field: str | None
    code: str
    message: str
    severity: str = "warning"

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_number": self.row_number,
            "field": self.field,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass
class VendorMappingResult:
    evidence_items: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[VendorMappingWarning] = field(default_factory=list)
    source_file: str | None = None

    @property
    def warning_count(self) -> int:
        return len(self.warnings)


def map_vendor_sample_file(
    input_path: str | Path,
    *,
    vendor_name: str,
    platform: str,
    query: str,
) -> VendorMappingResult:
    path = Path(input_path)
    records = _load_local_records(path)
    warnings: list[VendorMappingWarning] = []
    evidence_items: list[dict[str, Any]] = []
    for row_number, record in enumerate(records, start=2):
        item, row_warnings = map_vendor_record(
            record,
            row_number=row_number,
            vendor_name=vendor_name,
            default_platform=platform,
            default_query=query,
        )
        warnings.extend(row_warnings)
        if item:
            evidence_items.append(item)
    return VendorMappingResult(evidence_items=evidence_items, warnings=warnings, source_file=str(path))


def map_vendor_record(
    record: dict[str, Any],
    *,
    row_number: int,
    vendor_name: str,
    default_platform: str,
    default_query: str,
) -> tuple[dict[str, Any] | None, list[VendorMappingWarning]]:
    warnings: list[VendorMappingWarning] = []
    normalized_record = {_normalize_key(key): value for key, value in record.items()}
    used_keys: set[str] = set()

    def get(field_name: str) -> str:
        value, key = _field_value(record, normalized_record, field_name)
        if key:
            used_keys.add(key)
        return _sanitize_cell(value, row_number=row_number, field=field_name, warnings=warnings)

    source_provider = get("source_provider") or vendor_name
    platform = get("platform") or default_platform or "unknown_platform"
    source_type = _safe_source_type(get("source_type") or _infer_source_type(platform))
    query = get("query") or default_query
    content_id = get("content_id") or f"row_{row_number}"
    acquisition_mode = get("acquisition_mode")
    if acquisition_mode and _safe_token(acquisition_mode) != "data_vendor":
        warnings.append(
            _warning(
                row_number,
                "acquisition_mode",
                "acquisition_mode_forced_data_vendor",
                "Vendor sample rows are mapped as acquisition_mode=data_vendor for POC review.",
                "info",
            )
        )
    acquisition_mode = "data_vendor"

    title = get("title")
    body_text = get("body_text")
    comment_text = get("comment_text")
    parent_id = get("parent_id") or None
    root_id = get("root_id") or None
    url = get("url") or None
    evidence_type = _safe_evidence_type(get("evidence_type") or _infer_evidence_type(title, body_text, comment_text, parent_id, platform))
    created_at = _parse_timestamp(get("created_at"), row_number=row_number, field="created_at", warnings=warnings)
    collected_at = _parse_timestamp(get("collected_at"), row_number=row_number, field="collected_at", warnings=warnings)

    if not any((title, body_text, comment_text)) and evidence_type != "interaction_metric":
        warnings.append(_warning(row_number, None, "empty_evidence_row", "Row has no title, body_text, comment_text, or metric evidence."))
        return None, warnings

    compliance_metadata = {
        field_name: _compliance_value(get(field_name))
        for field_name in COMPLIANCE_FIELDS
    }
    vendor_attestation = _truthy(compliance_metadata.get("vendor_attestation"))
    risk_flags = _vendor_risk_flags(
        platform=platform,
        url=url,
        created_at=created_at,
        collection_method=str(compliance_metadata.get("collection_method") or ""),
        collection_basis=str(compliance_metadata.get("collection_basis") or ""),
        vendor_license_id=str(compliance_metadata.get("vendor_license_id") or ""),
        deletion_sync_supported=compliance_metadata.get("deletion_sync_supported"),
        personal_data_classification=str(compliance_metadata.get("personal_data_classification") or ""),
    )

    unknown_fields = _safe_unknown_fields(record, used_keys=used_keys, row_number=row_number, warnings=warnings)
    if any("secret" in warning.code for warning in warnings):
        risk_flags.append("possible_secret_redacted")
    if any(warning.code == "formula_like_text_plain" for warning in warnings):
        risk_flags.append("formula_like_text_plain")

    verification_status = "vendor_attested" if vendor_attestation else "needs_review"
    trust_label = "medium_low" if vendor_attestation else "unverified"
    trust_score = 0.52 if vendor_attestation else 0.25

    raw_data_safe = {
        "source_provider": source_provider,
        "query": query,
        "content_id": content_id,
        "collected_at": collected_at or "unknown",
        "repost_count": _safe_int(get("repost_count"), row_number=row_number, field="repost_count", warnings=warnings),
        "compliance_metadata": compliance_metadata,
        "unknown_fields": unknown_fields,
        "mapping_status": "offline_vendor_sample_only",
        "no_network_calls": True,
        "no_url_fetching": True,
        "no_scraping": True,
    }
    raw_data_safe = _sanitize_raw_metadata(raw_data_safe, row_number=row_number, warnings=warnings)

    author_id = get("author_id") or None
    author_name = get("author_name") or None
    language = get("language") or _infer_language(title, body_text, comment_text)
    item = {
        "evidence_id": _evidence_id(source_provider, platform, evidence_type, content_id, row_number),
        "case_id": None,
        "source_provider": source_provider,
        "platform": platform,
        "source_type": source_type,
        "acquisition_mode": acquisition_mode,
        "evidence_type": evidence_type,
        "title": title or None,
        "body_text": body_text or None,
        "comment_text": comment_text or None,
        "parent_id": parent_id,
        "root_id": root_id,
        "author_id": author_id,
        "author_name": author_name,
        "url": url,
        "created_at": created_at,
        "like_count": _safe_int(get("like_count"), row_number=row_number, field="like_count", warnings=warnings),
        "reply_count": _safe_int(get("reply_count"), row_number=row_number, field="reply_count", warnings=warnings),
        "share_count": _safe_int(get("share_count"), row_number=row_number, field="share_count", warnings=warnings),
        "view_count": _safe_int(get("view_count"), row_number=row_number, field="view_count", warnings=warnings),
        "raw_data_safe": raw_data_safe,
        "language": language,
        "content_visibility": "public_or_vendor_provided",
        "access_scope": "vendor_sample_poc",
        "provenance_type": "data_vendor",
        "verification_status": verification_status,
        "trust_score": trust_score,
        "trust_label": trust_label,
        "source_url_present": bool(url),
        "source_url": url,
        "source_platform_claim": platform,
        "source_capture_method": "vendor_sample_file",
        "user_attestation_required": False,
        "verification_notes": [
            "Vendor sample was mapped offline and is not official platform API evidence.",
            "No URL content was fetched during mapping.",
        ],
        "risk_flags": sorted(set(risk_flags)),
        "review_status": "review_needed",
        "ingestion_metadata": {
            "normalized_from": "vendor_sample_mapping",
            "source_record_id": content_id,
            "source_type": source_type,
            "acquisition_mode": "data_vendor",
            "warnings": [warning.code for warning in warnings],
            "safe_mode": {
                "real_api_calls": False,
                "url_fetching": False,
                "scraping": False,
                "secrets_exposed": False,
            },
        },
        "validation_warnings": [warning.to_dict() for warning in warnings],
    }
    return _remove_none(item), warnings


def write_jsonl(items: list[dict[str, Any]], output: io.TextIOBase) -> None:
    for item in items:
        output.write(json.dumps(item, ensure_ascii=False, sort_keys=True))
        output.write("\n")


def write_csv(items: list[dict[str, Any]], output: io.TextIOBase) -> None:
    headers = [
        "evidence_id",
        "source_provider",
        "platform",
        "source_type",
        "acquisition_mode",
        "evidence_type",
        "title",
        "body_text",
        "comment_text",
        "parent_id",
        "root_id",
        "author_id",
        "author_name",
        "url",
        "created_at",
        "like_count",
        "reply_count",
        "share_count",
        "view_count",
        "language",
        "provenance_type",
        "verification_status",
        "trust_label",
        "risk_flags",
        "raw_data_safe",
        "ingestion_metadata",
    ]
    writer = csv.DictWriter(output, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    for item in items:
        row = {}
        for header in headers:
            value = item.get(header, "")
            row[header] = json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else value
        writer.writerow(row)


def parse_vendor_timestamp(
    value: str,
    *,
    row_number: int,
    field: str,
    warnings: list[VendorMappingWarning],
) -> str | None:
    """Parse common vendor timestamp shapes without fetching or validating source URLs."""
    return _parse_timestamp(value, row_number=row_number, field=field, warnings=warnings)


def _load_local_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _load_csv_records(path)
    if suffix == ".json":
        return _load_json_records(path)
    raise ValueError("Unsupported vendor sample format. Use local CSV or JSON.")


def _load_csv_records(path: Path) -> list[dict[str, Any]]:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            text = data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("CSV encoding is not supported.")
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def _load_json_records(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, list):
        records = value
    elif isinstance(value, dict):
        records = value.get("records") or value.get("items") or value.get("data") or [value]
    else:
        raise ValueError("JSON sample must be an object, list, or object with records/items/data.")
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        raise ValueError("JSON sample records must be objects.")
    return records


def _field_value(
    original_record: dict[str, Any],
    normalized_record: dict[str, Any],
    field_name: str,
) -> tuple[Any, str | None]:
    for alias in FIELD_ALIASES[field_name]:
        normalized_alias = _normalize_key(alias)
        if normalized_alias in normalized_record:
            for key in original_record:
                if _normalize_key(key) == normalized_alias:
                    return original_record[key], key
    return "", None


def _safe_unknown_fields(
    record: dict[str, Any],
    *,
    used_keys: set[str],
    row_number: int,
    warnings: list[VendorMappingWarning],
) -> dict[str, Any]:
    known_aliases = {_normalize_key(alias) for aliases in FIELD_ALIASES.values() for alias in aliases}
    unknown: dict[str, Any] = {}
    for key, value in record.items():
        if key in used_keys or _normalize_key(key) in known_aliases:
            continue
        if _is_secret_key(key):
            warnings.append(_warning(row_number, key, "secret_field_omitted", "Secret-like vendor field was omitted from safe metadata."))
            continue
        unknown[key] = _sanitize_metadata_value(value, row_number=row_number, field=key, warnings=warnings)
    return unknown


def _sanitize_raw_metadata(value: Any, *, row_number: int, warnings: list[VendorMappingWarning]) -> Any:
    if isinstance(value, dict):
        safe: dict[str, Any] = {}
        for key, item in value.items():
            if _is_secret_key(key):
                warnings.append(_warning(row_number, key, "secret_field_omitted", "Secret-like metadata field was omitted."))
                continue
            safe[key] = _sanitize_raw_metadata(item, row_number=row_number, warnings=warnings)
        return safe
    if isinstance(value, list):
        return [_sanitize_raw_metadata(item, row_number=row_number, warnings=warnings) for item in value]
    return _redact_secret_text(str(value), row_number=row_number, field="raw_data_safe", warnings=warnings) if isinstance(value, str) else value


def _sanitize_metadata_value(value: Any, *, row_number: int, field: str, warnings: list[VendorMappingWarning]) -> Any:
    if isinstance(value, dict):
        return _sanitize_raw_metadata(value, row_number=row_number, warnings=warnings)
    if isinstance(value, list):
        return [_sanitize_metadata_value(item, row_number=row_number, field=field, warnings=warnings) for item in value]
    return _sanitize_cell(value, row_number=row_number, field=field, warnings=warnings)


def _sanitize_cell(value: Any, *, row_number: int, field: str, warnings: list[VendorMappingWarning]) -> str:
    text = " ".join(str(value or "").replace("\ufeff", "").split()).strip()
    if not text:
        return ""
    if text.startswith(FORMULA_PREFIXES):
        warnings.append(
            _warning(
                row_number,
                field,
                "formula_like_text_plain",
                "Formula-like cell was kept as plain text and not executed.",
                "info",
            )
        )
    return _redact_secret_text(text, row_number=row_number, field=field, warnings=warnings)


def _redact_secret_text(text: str, *, row_number: int, field: str, warnings: list[VendorMappingWarning]) -> str:
    redacted = SECRET_TEXT_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", text)
    if redacted != text:
        warnings.append(_warning(row_number, field, "secret_like_text_redacted", "Secret-like text was redacted."))
    return redacted


def _parse_timestamp(
    value: str,
    *,
    row_number: int,
    field: str,
    warnings: list[VendorMappingWarning],
) -> str | None:
    if not value:
        return None
    text = value.strip()
    try:
        if re.fullmatch(r"\d+(\.\d+)?", text):
            number = float(text)
            if number > 10_000_000_000:
                number = number / 1000
            return datetime.fromtimestamp(number, timezone.utc).isoformat().replace("+00:00", "Z")
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if parsed.tzinfo:
            return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return parsed.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OSError):
        warnings.append(_warning(row_number, field, "timestamp_unparsed", "Timestamp was kept as plain text because it was not parseable.", "info"))
        return text


def _safe_int(value: str, *, row_number: int, field: str, warnings: list[VendorMappingWarning]) -> int:
    if not value:
        return 0
    try:
        return max(0, int(float(str(value).replace(",", "").strip())))
    except ValueError:
        warnings.append(_warning(row_number, field, "invalid_number", f"{field} could not be parsed as a non-negative integer."))
        return 0


def _vendor_risk_flags(
    *,
    platform: str,
    url: str | None,
    created_at: str | None,
    collection_method: str,
    collection_basis: str,
    vendor_license_id: str,
    deletion_sync_supported: Any,
    personal_data_classification: str,
) -> list[str]:
    flags: list[str] = []
    normalized_method = collection_method.strip().lower()
    unclear_values = {"", "unknown", "unclear", "n/a", "na", "none"}
    if any(marker in normalized_method for marker in ("self_crawl", "self crawl", "scrape", "crawler", "public_web_crawl")):
        flags.append("self_crawled_public_web")
    if (
        collection_method.strip().lower() in unclear_values
        and collection_basis.strip().lower() in unclear_values
        and vendor_license_id.strip().lower() in unclear_values
    ):
        flags.append("source_unclear")
    if deletion_sync_supported in {"", None, "unknown"}:
        flags.append("deletion_sync_unknown")
    if not personal_data_classification or personal_data_classification.lower() in {"unknown", "unclear"}:
        flags.append("personal_data_unknown")
    if _safe_token(platform) not in KNOWN_PLATFORM_CLAIMS:
        flags.append("unsupported_platform_claim")
    if not url:
        flags.append("source_url_missing")
    if not created_at:
        flags.append("missing_timestamp")
    return flags


def _truthy(value: Any) -> bool:
    return _safe_token(str(value)) in {"true", "yes", "y", "1", "confirmed", "vendor_attested", "attested"}


def _compliance_value(value: str) -> str:
    return value if value != "" else "unknown"


def _safe_source_type(value: str) -> str:
    normalized = _safe_token(value)
    return normalized if normalized in SOURCE_TYPE_VALUES else "public_web"


def _safe_evidence_type(value: str) -> str:
    normalized = _safe_token(value)
    if normalized == "interaction_metrics":
        normalized = "interaction_metric"
    return normalized if normalized in EVIDENCE_TYPE_VALUES else "comment"


def _infer_source_type(platform: str) -> str:
    normalized = _safe_token(platform)
    if normalized in SOURCE_TYPE_VALUES:
        return normalized
    if normalized in {"the_paper", "jiemian", "xinhua", "people", "reuters", "bbc", "guardian", "news"}:
        return "news_site"
    if normalized in {"hupu", "tieba", "nga", "v2ex", "maimai", "douban", "zhihu"}:
        return "forum"
    return "public_web"


def _infer_evidence_type(title: str, body_text: str, comment_text: str, parent_id: str | None, platform: str) -> str:
    if comment_text and parent_id:
        return "reply"
    if comment_text:
        return "comment"
    if title and _safe_token(platform) in {"youtube", "douyin", "bilibili", "kuaishou", "tiktok"}:
        return "video"
    if title and body_text:
        return "article"
    if body_text:
        return "post"
    if title:
        return "title"
    return "uploaded_record"


def _infer_language(*values: str | None) -> str:
    joined = " ".join(value for value in values if value)
    if any("\u4e00" <= char <= "\u9fff" for char in joined):
        return "zh-CN"
    if joined:
        return "en-US"
    return "unknown"


def _evidence_id(source_provider: str, platform: str, evidence_type: str, content_id: str, row_number: int) -> str:
    raw = f"{source_provider}|{platform}|{evidence_type}|{content_id}|{row_number}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"evidence_vendor_{_safe_token(source_provider)[:24]}_{digest}"


def _remove_none(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if item is not None}


def _is_secret_key(key: str) -> bool:
    lowered = str(key).lower()
    return any(marker in lowered for marker in SECRET_KEY_MARKERS)


def _normalize_key(key: str) -> str:
    return re.sub(r"[\s_\-]+", "", str(key).strip().lower())


def _safe_token(value: str) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _warning(row_number: int | None, field: str | None, code: str, message: str, severity: str = "warning") -> VendorMappingWarning:
    return VendorMappingWarning(row_number=row_number, field=field, code=code, message=message, severity=severity)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map a local vendor CSV/JSON sample into Sentigraph EvidenceItem-like rows.")
    parser.add_argument("input_path", help="Local vendor sample CSV or JSON file.")
    parser.add_argument("--vendor-name", required=True, help="Vendor/provider name for safe metadata.")
    parser.add_argument("--platform", required=True, help="Default platform when rows omit platform.")
    parser.add_argument("--query", required=True, help="POC keyword/event query.")
    parser.add_argument("--output", help="Output file. Defaults to stdout.")
    parser.add_argument("--format", choices=("jsonl", "csv"), default="jsonl", help="Output format.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    result = map_vendor_sample_file(
        args.input_path,
        vendor_name=args.vendor_name,
        platform=args.platform,
        query=args.query,
    )
    if args.output:
        with Path(args.output).open("w", encoding="utf-8", newline="") as output_file:
            if args.format == "csv":
                write_csv(result.evidence_items, output_file)
            else:
                write_jsonl(result.evidence_items, output_file)
    else:
        if args.format == "csv":
            write_csv(result.evidence_items, sys.stdout)
        else:
            write_jsonl(result.evidence_items, sys.stdout)

    summary = {
        "source_file": result.source_file,
        "mapped_rows": len(result.evidence_items),
        "warning_count": result.warning_count,
        "warnings": [warning.to_dict() for warning in result.warnings],
        "safe_mode": {
            "vendor_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        },
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True), file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
