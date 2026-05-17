from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.main import app
from app.services import benchmark_summary


client = TestClient(app)


def test_latest_benchmark_summary_empty_state(monkeypatch, tmp_path) -> None:
    missing_path = tmp_path / "offline_benchmark_summary.json"
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", missing_path)

    response = client.get("/api/v1/benchmarks/latest")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "offline_benchmark_summary"
    assert body["available"] is False
    assert body["status"] == "missing"
    assert body["total_passed"] == 0
    assert body["total_failed"] == 0
    assert body["total_warnings"] == 0
    assert body["suites"] == []
    assert str(missing_path) not in response.text


def test_latest_benchmark_summary_valid_file_returns_safe_fields(monkeypatch, tmp_path) -> None:
    secret = "sk-secret-value-should-not-appear"
    unsafe_path = tmp_path / "should-not-appear" / "offline_benchmark_summary.json"
    summary_path = tmp_path / "offline_benchmark_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "benchmark_version": "v4.0_offline_benchmark_v1",
                "generated_at": "2026-05-17T00:00:00Z",
                "json_summary_path": str(unsafe_path),
                "total_passed": 3,
                "total_failed": 0,
                "total_warnings": 1,
                "suites": [
                    {
                        "suite": "sentiment",
                        "status": "pass",
                        "passed": 3,
                        "failed": 0,
                        "warnings": ["fixture warning"],
                        "cases": [{"details": {"secret": secret}}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)

    response = client.get("/api/v1/benchmarks/latest")

    assert response.status_code == 200
    body = response.json()
    assert body["available"] is True
    assert body["status"] == "available"
    assert body["benchmark_version"] == "v4.0_offline_benchmark_v1"
    assert body["generated_at"] == "2026-05-17T00:00:00Z"
    assert body["total_passed"] == 3
    assert body["total_failed"] == 0
    assert body["total_warnings"] == 1
    assert body["suites"] == [
        {
            "suite": "sentiment",
            "status": "pass",
            "passed": 3,
            "failed": 0,
            "warnings": ["fixture warning"],
        }
    ]
    assert "cases" not in response.text
    assert "json_summary_path" not in response.text
    assert str(unsafe_path) not in response.text
    assert secret not in response.text


def test_latest_benchmark_summary_malformed_file_fails_safely(monkeypatch, tmp_path) -> None:
    summary_path = tmp_path / "offline_benchmark_summary.json"
    summary_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)

    response = client.get("/api/v1/benchmarks/latest")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "offline_benchmark_summary"
    assert body["available"] is False
    assert body["status"] == "malformed"
    assert body["suites"] == []
    assert body["total_passed"] == 0
    assert body["total_failed"] == 0
    assert str(summary_path) not in response.text
