from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_source_catalog_returns_expected_categories() -> None:
    response = client.get("/api/v1/sources/catalog")

    assert response.status_code == 200
    body = response.json()
    category_ids = {category["category_id"] for category in body["categories"]}
    assert {
        "video_platforms",
        "news_media_sites",
        "forums_communities",
        "qa_sites",
        "complaint_review_sites",
        "finance_investor_forums",
        "social_platforms",
        "search_discovery",
        "rss",
        "user_uploaded_datasets",
        "manual_url_evidence",
        "data_vendor_future_integration",
    }.issubset(category_ids)
    assert body["total_categories"] >= 12
    assert body["safe_mode"]["static_metadata_only"] is True
    assert body["safe_mode"]["real_api_calls"] is False
    assert body["safe_mode"]["third_party_crawler_integrated"] is False


def test_source_catalog_marks_youtube_douyin_and_bilibili_statuses() -> None:
    body = client.get("/api/v1/sources/catalog").json()
    sources = {
        source["source_id"]: source
        for category in body["categories"]
        for source in category["sources"]
    }

    assert sources["youtube"]["feasibility_status"] == "green"
    assert sources["youtube"]["current_status"] == "real_capable_when_configured"
    assert "official_api_public" in sources["youtube"]["acquisition_modes"]

    assert sources["douyin"]["feasibility_status"] == "yellow"
    assert sources["douyin"]["current_status"] == "web_app_oauth_and_item_comment_pending"
    assert "official_api_oauth" in sources["douyin"]["acquisition_modes"]

    assert sources["bilibili"]["feasibility_status"] == "yellow"
    assert sources["bilibili"]["current_status"] == "official_permission_pending"


def test_source_catalog_does_not_expose_secrets_or_credentials() -> None:
    response_text = client.get("/api/v1/sources/catalog").text.lower()

    forbidden_fragments = [
        "youtube_api_key",
        "douyin_client_secret",
        "client_secret",
        "access_token",
        "refresh_token",
        "authorization:",
        "cookie:",
        ".env",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in response_text


def test_mediacrawler_is_not_integrated_in_catalog_or_product_code() -> None:
    body = client.get("/api/v1/sources/catalog").json()
    assert body["safe_mode"]["third_party_crawler_integrated"] is False

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
