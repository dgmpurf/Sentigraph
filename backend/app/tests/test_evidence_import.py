from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import CrawlStartResponse, PlatformCrawlMetadata
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.evidence_import import EVIDENCE_IMPORT_TEMPLATE_HEADERS, build_evidence_import_template_csv
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def configure_temp_case_store(tmp_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(tmp_path / "cases.json")))
    reset_case_store()


def test_csv_import_preview_and_commit_preserve_chinese_and_emoji() -> None:
    case_id = _create_case()
    payload = _file_payload("sample_evidence_import.csv")

    preview_response = client.post(f"/api/v1/cases/{case_id}/evidence/import/preview", json=payload)
    assert preview_response.status_code == 200
    preview = preview_response.json()
    assert preview["status"] == "preview_ready"
    assert preview["detected_format"] == "csv"
    assert preview["valid_row_count"] == 2
    assert preview["preview_rows"][0]["comment_text"] == "用户说官方回应太慢 😟"
    assert preview["safe_mode"]["raw_file_persisted"] is False
    assert preview["safe_mode"]["formulas_executed"] is False

    commit_response = client.post(f"/api/v1/cases/{case_id}/evidence/import/commit", json=payload)
    assert commit_response.status_code == 200
    committed = commit_response.json()
    assert committed["status"] == "committed"
    assert committed["imported_count"] == 2
    assert committed["source_distribution"] == {"uploaded_dataset": 2}
    assert committed["evidence_type_counts"] == {"comment": 2}
    assert any(item["comment_text"] == "用户说官方回应太慢 😟" for item in committed["evidence_items"])


def test_template_csv_endpoint_returns_expected_headers_and_safe_samples() -> None:
    response = client.get("/api/v1/evidence/import/template.csv")

    assert response.status_code == 200
    assert response.headers["content-type"].lower().startswith("text/csv")
    assert "charset=utf-8" in response.headers["content-type"].lower()
    assert response.headers["content-disposition"] == 'attachment; filename="sentigraph_evidence_import_template.csv"'
    lines = response.text.splitlines()
    assert lines[0].split(",") == EVIDENCE_IMPORT_TEMPLATE_HEADERS
    assert len(lines) == 4
    lowered = response.text.lower()
    for marker in ("api_key", "access_token", "refresh_token", "client_secret", "password", "cookie", "token", "secret"):
        assert marker not in lowered


def test_template_csv_sample_rows_can_be_previewed() -> None:
    case_id = _create_case()
    template_csv = build_evidence_import_template_csv()

    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/import/preview",
        json=_text_payload("sentigraph_evidence_import_template.csv", template_csv),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "preview_ready"
    assert body["valid_row_count"] == 3
    assert body["duplicate_row_count"] == 0
    evidence_types = {row["evidence_type"] for row in body["preview_rows"]}
    assert {"article", "video", "comment"}.issubset(evidence_types)
    assert any(row["comment_text"] == "用户反馈需要更透明的进展说明。" for row in body["preview_rows"])


def test_csv_import_redacts_secret_like_fields_and_plain_text_formulas() -> None:
    case_id = _create_case()
    csv_text = "\ufeffplatform,title,comment_text,api_key,created_at,like_count\nuploaded_dataset,=SUM(A1:A2),access_token=secret-marker should be removed,secret-marker,not-a-date,+7\n"
    payload = _text_payload("formula_secret.csv", csv_text)

    response = client.post(f"/api/v1/cases/{case_id}/evidence/import/preview", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "secret-marker" not in response.text
    assert body["preview_rows"][0]["title"] == "=SUM(A1:A2)"
    assert "access_token=[REDACTED]" in body["preview_rows"][0]["comment_text"]
    assert any(warning["code"] == "unverified_timestamp" for warning in body["warnings"] + body["preview_rows"][0]["warnings"])


def test_csv_import_invalid_rows_warn_and_duplicates_are_deduped() -> None:
    case_id = _create_case()
    csv_text = (
        "platform,title,comment_text,url\n"
        "uploaded_dataset,Duplicate title,Same public comment,https://example.test/1\n"
        "uploaded_dataset,Duplicate title,Same public comment,https://example.test/1\n"
        "uploaded_dataset,,,\n"
    )

    response = client.post(f"/api/v1/cases/{case_id}/evidence/import/preview", json=_text_payload("duplicates.csv", csv_text))

    assert response.status_code == 200
    body = response.json()
    assert body["valid_row_count"] == 1
    assert body["duplicate_row_count"] == 1
    assert any(warning["code"] == "duplicate_row" for warning in body["warnings"])


def test_xlsx_import_preview_uses_standard_library_parser() -> None:
    case_id = _create_case()
    payload = {
        "filename": "sample.xlsx",
        "content_base64": base64.b64encode(_simple_xlsx()).decode("ascii"),
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/import/preview", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["detected_format"] == "xlsx"
    assert body["valid_row_count"] == 1
    assert body["preview_rows"][0]["title"] == "XLSX public article"
    assert body["preview_rows"][0]["comment_text"] == "Excel 评论保留中文 😄"


def test_imported_evidence_feeds_analysis_when_no_raw_comments() -> None:
    case_id = _create_case()
    commit_response = client.post(f"/api/v1/cases/{case_id}/evidence/import/commit", json=_file_payload("sample_evidence_import.csv"))
    assert commit_response.status_code == 200

    run_response = client.post(f"/api/v1/cases/{case_id}/run")

    assert run_response.status_code == 200
    body = run_response.json()
    assert body["analysis_input_source"] == "case_evidence_items"
    assert body["analysis_result"]["analysis_input_source"] == "case_evidence_items"
    assert body["report"]["evidence_item_count"] == 2
    assert any("官方回应太慢" in comment for comment in body["report"]["representative_comments"])


def test_raw_case_data_still_wins_over_imported_evidence(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])
    assert client.post(f"/api/v1/cases/{case_id}/evidence/import/commit", json=_file_payload("sample_evidence_import.csv")).status_code == 200

    def fake_start_crawl(payload):
        return CrawlStartResponse(
            project_id="project_crawl_youtube",
            crawl_task_id="task_youtube_fixture",
            status="completed",
            message="Fixture crawl.",
            platform_metadata=[
                PlatformCrawlMetadata(
                    platform="youtube",
                    adapter_mode="real",
                    source_type="youtube_data_api_v3",
                    fallback_used=False,
                    credential_present=True,
                    post_count=1,
                    comment_count=1,
                )
            ],
            raw_posts=[
                RawPost(
                    platform="youtube",
                    post_id="yt_video_001",
                    author_id="yt_channel_001",
                    author_name="Fixture YouTube Channel",
                    title="YouTube public video title",
                    content="Mocked official response.",
                    created_at="2026-05-25T09:00:00Z",
                    url="https://www.youtube.com/watch?v=yt_video_001",
                    raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
                )
            ],
            raw_comments=[
                RawComment(
                    platform="youtube",
                    post_id="yt_video_001",
                    comment_id="yt_comment_001",
                    author_id="yt_commenter_001",
                    author_name="Fixture commenter",
                    content="YouTube raw comment should win over uploaded evidence.",
                    created_at="2026-05-25T09:02:00Z",
                    url="https://www.youtube.com/watch?v=yt_video_001&lc=yt_comment_001",
                    raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
                )
            ],
        )

    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", fake_start_crawl)
    assert client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3}).status_code == 200
    run_response = client.post(f"/api/v1/cases/{case_id}/run")

    assert run_response.status_code == 200
    body = run_response.json()
    assert body["analysis_input_source"] == "case_raw_data"
    assert body["raw_comment_count"] == 1
    assert any("YouTube raw comment should win" in comment for comment in body["report"]["representative_comments"])


def test_import_rejects_unknown_binary_and_does_not_reference_third_party_crawler() -> None:
    case_id = _create_case()
    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/import/preview",
        json={"filename": "payload.bin", "content_base64": base64.b64encode(b"\x00\x01binary").decode("ascii")},
    )

    assert response.status_code == 400
    repo_root = Path(__file__).resolve().parents[3]
    product_paths = [
        repo_root / "backend" / "app" / "api",
        repo_root / "backend" / "app" / "schemas",
        repo_root / "backend" / "app" / "services",
        repo_root / "frontend" / "src",
    ]
    matches: list[str] = []
    for product_path in product_paths:
        for file_path in product_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in {".py", ".js", ".jsx", ".ts", ".tsx"}:
                text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
                if "mediacrawler" in text or "media crawler" in text:
                    matches.append(str(file_path.relative_to(repo_root)))
    assert matches == []


def _create_case(platforms: list[str] | None = None) -> str:
    response = client.post(
        "/api/v1/cases",
        json={"keyword": "Tesla", "platforms": platforms or ["uploaded_dataset"], "title": "Evidence Import QA Case"},
    )
    assert response.status_code == 200
    return response.json()["case_id"]


def _file_payload(name: str) -> dict[str, str]:
    path = Path(__file__).parent / "fixtures" / "evidence" / name
    return {"filename": name, "content_base64": base64.b64encode(path.read_bytes()).decode("ascii")}


def _text_payload(name: str, text: str) -> dict[str, str]:
    return {"filename": name, "content_base64": base64.b64encode(text.encode("utf-8")).decode("ascii")}


def _simple_xlsx() -> bytes:
    shared_strings = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="6" uniqueCount="6">
  <si><t>platform</t></si>
  <si><t>title</t></si>
  <si><t>comment_text</t></si>
  <si><t>uploaded_dataset</t></si>
  <si><t>XLSX public article</t></si>
  <si><t>Excel 评论保留中文 😄</t></si>
</sst>"""
    sheet = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="s"><v>0</v></c>
      <c r="B1" t="s"><v>1</v></c>
      <c r="C1" t="s"><v>2</v></c>
    </row>
    <row r="2">
      <c r="A2" t="s"><v>3</v></c>
      <c r="B2" t="s"><v>4</v></c>
      <c r="C2" t="s"><v>5</v></c>
    </row>
  </sheetData>
</worksheet>"""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as workbook:
        workbook.writestr("[Content_Types].xml", "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\"/>")
        workbook.writestr("xl/sharedStrings.xml", shared_strings)
        workbook.writestr("xl/worksheets/sheet1.xml", sheet)
    return buffer.getvalue()
