from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from typing import Any
from xml.etree import ElementTree as ET

from app.schemas.evidence import (
    EvidenceAcquisitionMode,
    EvidenceImportColumnMapping,
    EvidenceImportCommitRequest,
    EvidenceImportCommitResult,
    EvidenceImportPreviewRequest,
    EvidenceImportPreviewResult,
    EvidenceImportRowPreview,
    EvidenceImportValidationWarning,
    EvidenceItem,
    EvidenceNormalizationMetadata,
    EvidenceSourceType,
    EvidenceType,
)
from app.services.evidence_ingestion import (
    evidence_source_distribution,
    evidence_type_distribution,
    sanitize_raw_data,
)


MAX_IMPORT_BYTES = 1_500_000
MAX_XLSX_UNCOMPRESSED_BYTES = 5_000_000
SECRET_MARKERS = {
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
}
VALID_SOURCE_TYPES = {
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
VALID_ACQUISITION_MODES = {
    "official_api_public",
    "official_api_oauth",
    "public_parser",
    "search_discovery",
    "user_upload",
    "manual_url",
    "data_vendor",
    "mock_fixture",
}
VALID_EVIDENCE_TYPES = {
    "video",
    "article",
    "post",
    "comment",
    "reply",
    "title",
    "body_text",
    "metadata",
    "interaction_metric",
    "interaction_metrics",
    "search_result",
    "uploaded_record",
}
FIELD_SYNONYMS = {
    "platform": ["platform", "平台", "source_platform"],
    "source_type": ["source_type", "source", "来源类型"],
    "acquisition_mode": ["acquisition_mode", "mode", "获取方式", "采集方式"],
    "evidence_type": ["evidence_type", "type", "内容类型", "证据类型"],
    "title": ["title", "标题", "视频标题", "article_title", "video_title"],
    "body_text": ["body_text", "body", "正文", "内容", "description", "content", "text"],
    "comment_text": ["comment_text", "comment", "评论", "评论内容", "reply_text"],
    "parent_id": ["parent_id", "父评论id", "parent_comment_id"],
    "root_id": ["root_id", "post_id", "video_id", "article_id", "item_id"],
    "author_id": ["author_id", "user_id", "作者id", "用户id"],
    "author_name": ["author_name", "author", "nickname", "用户名", "作者", "昵称"],
    "url": ["url", "link", "链接", "source_url"],
    "created_at": ["created_at", "published_at", "time", "timestamp", "发布时间", "创建时间"],
    "like_count": ["like_count", "likes", "点赞", "点赞数"],
    "reply_count": ["reply_count", "comments", "评论数", "回复数"],
    "share_count": ["share_count", "shares", "分享数", "转发数"],
    "view_count": ["view_count", "views", "播放量", "浏览量"],
    "language": ["language", "lang", "语言"],
}


class EvidenceImportError(ValueError):
    """Safe import error shown to users without leaking local paths or secrets."""


def preview_evidence_import(case_id: str, request: EvidenceImportPreviewRequest) -> EvidenceImportPreviewResult:
    parsed = _parse_import_request(request)
    normalized = _normalize_import_rows(case_id, parsed["rows"], parsed["headers"], request.column_mapping, request.max_rows)
    preview_rows = [_to_preview_row(item, warnings) for item, warnings in normalized["items_with_warnings"][: request.preview_limit]]
    return EvidenceImportPreviewResult(
        case_id=case_id,
        filename=request.filename,
        status="preview_ready" if normalized["items"] else "empty",
        detected_format=parsed["format"],
        detected_columns=parsed["headers"],
        column_mapping=normalized["mapping"],
        total_rows=normalized["total_rows"],
        valid_row_count=len(normalized["items"]),
        duplicate_row_count=normalized["duplicate_count"],
        skipped_row_count=normalized["skipped_count"],
        preview_rows=preview_rows,
        warnings=parsed["warnings"] + normalized["warnings"],
    )


def build_imported_evidence_items(
    case_id: str,
    request: EvidenceImportCommitRequest,
) -> tuple[list[EvidenceItem], dict[str, Any]]:
    parsed = _parse_import_request(request)
    normalized = _normalize_import_rows(case_id, parsed["rows"], parsed["headers"], request.column_mapping, request.max_rows)
    metadata = {
        "filename": request.filename,
        "detected_format": parsed["format"],
        "duplicate_count": normalized["duplicate_count"],
        "skipped_count": normalized["skipped_count"],
        "warnings": parsed["warnings"] + normalized["warnings"],
    }
    return normalized["items"], metadata


def build_import_commit_result(
    *,
    case_id: str,
    request: EvidenceImportCommitRequest,
    imported_items: list[EvidenceItem],
    total_items: list[EvidenceItem],
    metadata: dict[str, Any],
) -> EvidenceImportCommitResult:
    return EvidenceImportCommitResult(
        case_id=case_id,
        filename=request.filename,
        status="committed" if imported_items else "empty",
        detected_format=metadata.get("detected_format"),
        imported_count=len(imported_items),
        total_evidence_item_count=len(total_items),
        duplicate_row_count=int(metadata.get("duplicate_count") or 0),
        skipped_row_count=int(metadata.get("skipped_count") or 0),
        evidence_items=imported_items,
        source_distribution=evidence_source_distribution(total_items),
        evidence_type_counts=evidence_type_distribution(total_items),
        warnings=metadata.get("warnings") or [],
    )


def _parse_import_request(request: EvidenceImportPreviewRequest) -> dict[str, Any]:
    data = _request_bytes(request)
    file_format = _detect_format(request.filename, data)
    if file_format == "csv":
        headers, rows, warnings = _parse_csv(data)
    else:
        headers, rows, warnings = _parse_xlsx(data)
    if not headers:
        raise EvidenceImportError("Import file must contain a header row.")
    return {
        "format": file_format,
        "headers": headers,
        "rows": rows,
        "warnings": warnings,
    }


def _request_bytes(request: EvidenceImportPreviewRequest) -> bytes:
    if request.content_base64:
        try:
            data = base64.b64decode(request.content_base64, validate=True)
        except Exception as exc:  # pragma: no cover - exact decoder exception varies
            raise EvidenceImportError("Invalid base64 file content.") from exc
    elif request.content_text is not None:
        data = request.content_text.encode("utf-8")
    else:
        raise EvidenceImportError("No file content was provided.")
    if not data:
        raise EvidenceImportError("Import file is empty.")
    if len(data) > MAX_IMPORT_BYTES:
        raise EvidenceImportError("Import file is too large for local preview.")
    return data


def _detect_format(filename: str, data: bytes) -> str:
    lowered = filename.lower().strip()
    if lowered.endswith(".csv") or lowered.endswith(".txt"):
        if b"\x00" in data[:1024]:
            raise EvidenceImportError("CSV import rejected binary-looking content.")
        return "csv"
    if lowered.endswith(".xlsx"):
        if not data.startswith(b"PK"):
            raise EvidenceImportError("XLSX import rejected malformed workbook content.")
        return "xlsx"
    if lowered.endswith((".xlsm", ".xls", ".xlsb")):
        raise EvidenceImportError("Only macro-free .xlsx workbooks are supported.")
    raise EvidenceImportError("Unsupported import format. Use CSV or macro-free XLSX.")


def _parse_csv(data: bytes) -> tuple[list[str], list[dict[str, str]], list[EvidenceImportValidationWarning]]:
    warnings: list[EvidenceImportValidationWarning] = []
    decoded = None
    used_encoding = ""
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            decoded = data.decode(encoding)
            used_encoding = encoding
            break
        except UnicodeDecodeError:
            continue
    if decoded is None:
        raise EvidenceImportError("CSV encoding is not supported.")
    if used_encoding in {"gb18030", "gbk"}:
        warnings.append(_warning("encoding_fallback", f"CSV decoded with {used_encoding} fallback.", severity="info"))
    sample = decoded[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(decoded), dialect=dialect)
    headers = [_clean_header(header) for header in reader.fieldnames or [] if _clean_header(header)]
    rows: list[dict[str, str]] = []
    for row in reader:
        rows.append({_clean_header(key): _cell_text(value) for key, value in row.items() if _clean_header(key)})
    return headers, rows, warnings


def _parse_xlsx(data: bytes) -> tuple[list[str], list[dict[str, str]], list[EvidenceImportValidationWarning]]:
    warnings: list[EvidenceImportValidationWarning] = []
    with zipfile.ZipFile(io.BytesIO(data)) as workbook:
        names = set(workbook.namelist())
        if "xl/vbaProject.bin" in names:
            raise EvidenceImportError("Macro-enabled workbooks are not supported.")
        uncompressed = sum(info.file_size for info in workbook.infolist())
        if uncompressed > MAX_XLSX_UNCOMPRESSED_BYTES:
            raise EvidenceImportError("XLSX workbook is too large for local preview.")
        shared_strings = _read_shared_strings(workbook)
        worksheet_name = "xl/worksheets/sheet1.xml"
        if worksheet_name not in names:
            worksheet_candidates = sorted(name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"))
            if not worksheet_candidates:
                raise EvidenceImportError("XLSX workbook does not contain a readable worksheet.")
            worksheet_name = worksheet_candidates[0]
        root = ET.fromstring(workbook.read(worksheet_name))
    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    table_rows: list[list[str]] = []
    formula_found = False
    for row_node in root.findall(".//x:sheetData/x:row", namespace):
        cells: dict[int, str] = {}
        for cell_node in row_node.findall("x:c", namespace):
            column_index = _column_index(cell_node.attrib.get("r", ""))
            if column_index < 0:
                continue
            text, had_formula = _xlsx_cell_text(cell_node, shared_strings, namespace)
            formula_found = formula_found or had_formula
            cells[column_index] = _cell_text(text)
        if cells:
            max_index = max(cells)
            table_rows.append([cells.get(index, "") for index in range(max_index + 1)])
    if formula_found:
        warnings.append(_warning("formula_plain_text", "Workbook formulas were imported as plain text only.", severity="info"))
    if not table_rows:
        return [], [], warnings
    headers = [_clean_header(value) for value in table_rows[0]]
    rows = []
    for row_values in table_rows[1:]:
        rows.append({headers[index]: row_values[index] if index < len(row_values) else "" for index in range(len(headers)) if headers[index]})
    return [header for header in headers if header], rows, warnings


def _read_shared_strings(workbook: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in workbook.namelist():
        return []
    root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    namespace = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    values: list[str] = []
    for item in root.findall(".//x:si", namespace):
        texts = [node.text or "" for node in item.findall(".//x:t", namespace)]
        values.append("".join(texts))
    return values


def _xlsx_cell_text(cell_node: ET.Element, shared_strings: list[str], namespace: dict[str, str]) -> tuple[str, bool]:
    formula = cell_node.find("x:f", namespace)
    if formula is not None:
        return f"={formula.text or ''}", True
    cell_type = cell_node.attrib.get("t")
    value_node = cell_node.find("x:v", namespace)
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell_node.findall(".//x:t", namespace)), False
    value = value_node.text if value_node is not None and value_node.text is not None else ""
    if cell_type == "s" and value:
        try:
            return shared_strings[int(value)], False
        except (ValueError, IndexError):
            return "", False
    return value, False


def _column_index(cell_reference: str) -> int:
    letters = "".join(char for char in cell_reference if char.isalpha()).upper()
    if not letters:
        return -1
    index = 0
    for char in letters:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def _normalize_import_rows(
    case_id: str,
    rows: list[dict[str, str]],
    headers: list[str],
    provided_mapping: EvidenceImportColumnMapping,
    max_rows: int,
) -> dict[str, Any]:
    mapping = _build_mapping(headers, provided_mapping)
    warnings: list[EvidenceImportValidationWarning] = []
    items: list[EvidenceItem] = []
    items_with_warnings: list[tuple[EvidenceItem, list[EvidenceImportValidationWarning]]] = []
    seen_hashes: set[str] = set()
    duplicate_count = 0
    skipped_count = 0
    total_rows = 0

    for index, row in enumerate(rows, start=2):
        if total_rows >= max_rows:
            warnings.append(_warning("row_limit_reached", f"Only the first {max_rows} rows were processed.", severity="warning"))
            break
        if _is_blank_row(row):
            continue
        total_rows += 1
        item, row_warnings = _row_to_evidence_item(case_id, row, index, mapping)
        if item is None:
            skipped_count += 1
            warnings.extend(row_warnings)
            continue
        content_hash = _content_hash(item)
        if content_hash in seen_hashes:
            duplicate_count += 1
            warnings.append(_warning("duplicate_row", "Duplicate row skipped by content hash.", row_number=index, severity="info"))
            continue
        seen_hashes.add(content_hash)
        item = item.model_copy(update={"evidence_id": f"evidence_import_{content_hash[:16]}"}, deep=True)
        items.append(item)
        items_with_warnings.append((item, row_warnings))

    return {
        "items": items,
        "items_with_warnings": items_with_warnings,
        "mapping": mapping,
        "warnings": warnings,
        "duplicate_count": duplicate_count,
        "skipped_count": skipped_count,
        "total_rows": total_rows,
    }


def _build_mapping(headers: list[str], provided_mapping: EvidenceImportColumnMapping) -> EvidenceImportColumnMapping:
    normalized_headers = {_normalize_header(header): header for header in headers}
    values: dict[str, str | None] = {}
    provided = provided_mapping.model_dump()
    for field_name, synonyms in FIELD_SYNONYMS.items():
        provided_column = provided.get(field_name)
        if provided_column and _normalize_header(provided_column) in normalized_headers:
            values[field_name] = normalized_headers[_normalize_header(provided_column)]
            continue
        values[field_name] = None
        for synonym in synonyms:
            if _normalize_header(synonym) in normalized_headers:
                values[field_name] = normalized_headers[_normalize_header(synonym)]
                break
    return EvidenceImportColumnMapping(**values)


def _row_to_evidence_item(
    case_id: str,
    row: dict[str, str],
    row_number: int,
    mapping: EvidenceImportColumnMapping,
) -> tuple[EvidenceItem | None, list[EvidenceImportValidationWarning]]:
    row_warnings: list[EvidenceImportValidationWarning] = []
    def get(field: str) -> str:
        column = getattr(mapping, field)
        if column and _is_secret_column(column):
            row_warnings.append(_warning("secret_column_redacted", "Secret-like source column was not imported.", row_number=row_number, field=field))
            return ""
        return _redact_secret_text(_mapped_value(row, mapping, field), row_number, field, row_warnings)

    platform = get("platform") or "uploaded_dataset"
    source_type = _safe_source_type(get("source_type"))
    acquisition_mode = _safe_acquisition_mode(get("acquisition_mode"))
    title = get("title")
    body_text = get("body_text")
    comment_text = get("comment_text")
    parent_id = get("parent_id") or None
    root_id = get("root_id") or None
    like_count = _safe_int(get("like_count"), row_number, "like_count", row_warnings)
    reply_count = _safe_int(get("reply_count"), row_number, "reply_count", row_warnings)
    share_count = _safe_int(get("share_count"), row_number, "share_count", row_warnings)
    view_count = _safe_int(get("view_count"), row_number, "view_count", row_warnings)
    has_metrics = any((like_count, reply_count, share_count, view_count))
    explicit_type = get("evidence_type")
    evidence_type = _safe_evidence_type(explicit_type) if explicit_type else _infer_evidence_type(title, body_text, comment_text, parent_id, row, has_metrics)
    if not _has_meaningful_content(evidence_type, title, body_text, comment_text, like_count, reply_count, share_count, view_count):
        row_warnings.append(_warning("empty_evidence_row", "Row has no importable evidence text or metrics.", row_number=row_number))
        return None, row_warnings
    created_at = _safe_timestamp(get("created_at"), row_number, row_warnings)
    raw_data_safe = sanitize_raw_data(
        {
            "import_row_number": row_number,
            "source_file_type": "user_upload",
            "mapped_columns": {field: column for field, column in mapping.model_dump().items() if column},
        }
    )
    return (
        EvidenceItem(
            evidence_id="",
            case_id=case_id,
            platform=platform,
            source_type=source_type,
            acquisition_mode=acquisition_mode,
            evidence_type=evidence_type,
            title=title or None,
            body_text=body_text or None,
            comment_text=comment_text or None,
            parent_id=parent_id,
            root_id=root_id,
            author_id=get("author_id") or None,
            author_name=get("author_name") or None,
            url=get("url") or None,
            created_at=created_at,
            like_count=like_count,
            reply_count=reply_count,
            share_count=share_count,
            view_count=view_count,
            raw_data_safe=raw_data_safe,
            language=get("language") or _infer_language(title, body_text, comment_text),
            content_visibility="public_or_user_provided",
            access_scope="user_provided_lawful_source",
            ingestion_metadata=EvidenceNormalizationMetadata(
                normalized_from="user_upload_import",
                source_record_id=f"row_{row_number}",
                source_type=source_type,
                acquisition_mode=acquisition_mode,
                normalized_at=datetime.now(timezone.utc),
                warnings=[warning.code for warning in row_warnings],
            ),
        ),
        row_warnings,
    )


def _mapped_value(row: dict[str, str], mapping: EvidenceImportColumnMapping, field: str) -> str:
    column = getattr(mapping, field)
    if not column:
        return ""
    return _cell_text(row.get(column, ""))


def _infer_evidence_type(
    title: str,
    body_text: str,
    comment_text: str,
    parent_id: str | None,
    row: dict[str, str],
    has_metrics: bool,
) -> EvidenceType:
    if comment_text and parent_id:
        return "reply"
    if comment_text:
        return "comment"
    if title and _looks_video_like(row):
        return "video"
    if title and body_text:
        return "article"
    if body_text:
        return "post"
    if title:
        return "title"
    if has_metrics or any(_cell_text(row.get(key, "")) for key in ("like_count", "reply_count", "share_count", "view_count")):
        return "interaction_metric"
    return "uploaded_record"


def _looks_video_like(row: dict[str, str]) -> bool:
    searchable = " ".join(f"{key} {value}" for key, value in row.items()).lower()
    return any(marker in searchable for marker in ("video", "youtube", "youtu.be", "bilibili", "douyin", "tiktok", "kuaishou"))


def _has_meaningful_content(
    evidence_type: str,
    title: str,
    body_text: str,
    comment_text: str,
    like_count: int,
    reply_count: int,
    share_count: int,
    view_count: int,
) -> bool:
    if title or body_text or comment_text:
        return True
    return evidence_type == "interaction_metric" and any((like_count, reply_count, share_count, view_count))


def _safe_source_type(value: str) -> EvidenceSourceType:
    normalized = _safe_token(value or "uploaded_dataset")
    return normalized if normalized in VALID_SOURCE_TYPES else "uploaded_dataset"  # type: ignore[return-value]


def _safe_acquisition_mode(value: str) -> EvidenceAcquisitionMode:
    normalized = _safe_token(value or "user_upload")
    return normalized if normalized in VALID_ACQUISITION_MODES else "user_upload"  # type: ignore[return-value]


def _safe_evidence_type(value: str) -> EvidenceType:
    normalized = _safe_token(value or "comment")
    if normalized == "interaction_metrics":
        normalized = "interaction_metric"
    return normalized if normalized in VALID_EVIDENCE_TYPES else "comment"  # type: ignore[return-value]


def _safe_int(value: str, row_number: int, field: str, warnings: list[EvidenceImportValidationWarning]) -> int:
    if value == "":
        return 0
    try:
        parsed = int(float(value.replace(",", "")))
    except ValueError:
        warnings.append(_warning("invalid_number", f"{field} could not be parsed as a number.", row_number=row_number, field=field))
        return 0
    return max(0, parsed)


def _safe_timestamp(value: str, row_number: int, warnings: list[EvidenceImportValidationWarning]) -> str | None:
    if not value:
        return None
    text = _cell_text(value)
    if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", text):
        return text
    if "T" in text or " " in text:
        return text
    warnings.append(_warning("unverified_timestamp", "Timestamp kept as plain text because format was not recognized.", row_number=row_number, field="created_at", severity="info"))
    return text


def _to_preview_row(
    item: EvidenceItem,
    warnings: list[EvidenceImportValidationWarning],
) -> EvidenceImportRowPreview:
    row_number = int(item.raw_data_safe.get("import_row_number") or 0)
    return EvidenceImportRowPreview(
        row_number=row_number,
        evidence_id=item.evidence_id,
        platform=item.platform,
        source_type=item.source_type,
        acquisition_mode=item.acquisition_mode,
        evidence_type=item.evidence_type,
        title=item.title,
        body_text=_clip(item.body_text, 180) if item.body_text else None,
        comment_text=_clip(item.comment_text, 180) if item.comment_text else None,
        author_name=item.author_name,
        url=item.url,
        created_at=item.created_at,
        like_count=item.like_count,
        reply_count=item.reply_count,
        share_count=item.share_count,
        view_count=item.view_count,
        warnings=warnings,
    )


def _content_hash(item: EvidenceItem) -> str:
    payload = {
        "platform": item.platform,
        "source_type": item.source_type,
        "evidence_type": item.evidence_type,
        "title": item.title or "",
        "body_text": item.body_text or "",
        "comment_text": item.comment_text or "",
        "parent_id": item.parent_id or "",
        "root_id": item.root_id or "",
        "url": item.url or "",
        "created_at": item.created_at or "",
    }
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _cell_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\ufeff", "").split()).strip()


def _clean_header(value: Any) -> str:
    return _cell_text(value)


def _normalize_header(value: str) -> str:
    return re.sub(r"[\s_\-]+", "", str(value).strip().lower())


def _safe_token(value: str) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _is_blank_row(row: dict[str, str]) -> bool:
    return not any(_cell_text(value) for value in row.values())


def _redact_secret_text(
    value: str,
    row_number: int,
    field: str,
    warnings: list[EvidenceImportValidationWarning],
) -> str:
    if not value:
        return ""
    redacted = re.sub(
        r"(?i)\b(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|cookie)\b\s*[:=]\s*[^,\s;]+",
        lambda match: f"{match.group(1)}=[REDACTED]",
        value,
    )
    if redacted != value:
        warnings.append(_warning("secret_like_text_redacted", "Secret-like text was redacted.", row_number=row_number, field=field))
    return redacted


def _is_secret_column(column: str) -> bool:
    lowered = column.lower()
    return any(marker in lowered for marker in SECRET_MARKERS)


def _warning(
    code: str,
    message: str,
    *,
    row_number: int | None = None,
    field: str | None = None,
    severity: str = "warning",
) -> EvidenceImportValidationWarning:
    return EvidenceImportValidationWarning(
        row_number=row_number,
        field=field,
        code=code,
        message=message,
        severity=severity,  # type: ignore[arg-type]
    )


def _infer_language(*values: str | None) -> str:
    joined = " ".join(value for value in values if value)
    if any("\u4e00" <= char <= "\u9fff" for char in joined):
        return "zh-CN"
    if joined:
        return "en-US"
    return "unknown"


def _clip(value: str | None, length: int) -> str:
    text = _cell_text(value)
    return text[:length]
