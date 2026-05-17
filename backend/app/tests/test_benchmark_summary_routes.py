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
                "benchmark_id": "benchmark_latest",
                "generated_at": "2026-05-17T00:00:00Z",
                "duration_seconds": 0.12,
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
    assert body["benchmark_id"] == "benchmark_latest"
    assert body["benchmark_version"] == "v4.0_offline_benchmark_v1"
    assert body["generated_at"] == "2026-05-17T00:00:00Z"
    assert body["duration_seconds"] == 0.12
    assert body["total_passed"] == 3
    assert body["total_failed"] == 0
    assert body["total_warnings"] == 1
    assert body["suites"] == [
        {
            "suite": "sentiment",
            "status": "pass",
            "case_count": 3,
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


def test_benchmark_history_empty_state(monkeypatch, tmp_path) -> None:
    missing_dir = tmp_path / "history"
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_HISTORY_DIR", missing_dir)

    response = client.get("/api/v1/benchmarks/history")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "offline_benchmark_history"
    assert body["available"] is False
    assert body["status"] == "missing"
    assert body["entries"] == []
    assert str(missing_dir) not in response.text


def test_benchmark_history_list_returns_safe_entries(monkeypatch, tmp_path) -> None:
    history_dir = tmp_path / "history"
    history_dir.mkdir()
    secret = "sk-history-secret"
    (history_dir / "20260517T000000Z.json").write_text(
        json.dumps(
            _history_payload(
                benchmark_id="benchmark_20260517T000000z",
                generated_at="2026-05-17T00:00:00Z",
                total_passed=7,
                total_failed=0,
                total_warnings=1,
                suites=[
                    {
                        "suite": "sentiment",
                        "status": "pass",
                        "passed": 7,
                        "failed": 0,
                        "warnings": ["fixture warning"],
                        "cases": [{"details": {"secret": secret}}],
                    }
                ],
                regression_detected=False,
            )
        ),
        encoding="utf-8",
    )
    (history_dir / "malformed.json").write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_HISTORY_DIR", history_dir)

    response = client.get("/api/v1/benchmarks/history")

    assert response.status_code == 200
    body = response.json()
    assert body["available"] is True
    assert body["status"] == "available"
    assert body["total_entries"] == 1
    assert body["malformed_entries"] == 1
    assert body["entries"][0]["benchmark_id"] == "benchmark_20260517T000000z"
    assert body["entries"][0]["total_passed"] == 7
    assert body["entries"][0]["suites"][0]["suite"] == "sentiment"
    assert "cases" not in response.text
    assert secret not in response.text
    assert str(history_dir) not in response.text


def test_benchmark_regression_no_history(monkeypatch, tmp_path) -> None:
    summary_path = tmp_path / "offline_benchmark_summary.json"
    summary_path.write_text(
        json.dumps(
            _latest_payload(
                benchmark_id="benchmark_latest",
                generated_at="2026-05-17T01:00:00Z",
                total_passed=7,
                total_failed=0,
                total_warnings=0,
            )
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_HISTORY_DIR", tmp_path / "missing-history")

    response = client.get("/api/v1/benchmarks/regression")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "offline_benchmark_regression"
    assert body["available"] is False
    assert body["status"] == "no_history"
    assert body["regression_detected"] is False
    assert body["changed_suites"] == []
    assert body["latest_total_failed"] == 0
    assert str(summary_path) not in response.text


def test_benchmark_regression_no_change(monkeypatch, tmp_path) -> None:
    summary_path, history_dir = _write_latest_and_history(
        tmp_path,
        latest=_latest_payload(
            benchmark_id="benchmark_latest",
            generated_at="2026-05-17T01:00:00Z",
            total_passed=7,
            total_failed=0,
            total_warnings=0,
        ),
        previous=_history_payload(
            benchmark_id="benchmark_previous",
            generated_at="2026-05-17T00:00:00Z",
            total_passed=7,
            total_failed=0,
            total_warnings=0,
        ),
    )
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_HISTORY_DIR", history_dir)

    response = client.get("/api/v1/benchmarks/regression")

    assert response.status_code == 200
    body = response.json()
    assert body["available"] is True
    assert body["status"] == "no_regression"
    assert body["regression_detected"] is False
    assert body["changed_suites"] == []
    assert body["previous_total_failed"] == 0
    assert body["latest_total_failed"] == 0


def test_benchmark_regression_detects_increased_failures(monkeypatch, tmp_path) -> None:
    summary_path, history_dir = _write_latest_and_history(
        tmp_path,
        latest=_latest_payload(
            benchmark_id="benchmark_latest",
            generated_at="2026-05-17T01:00:00Z",
            total_passed=6,
            total_failed=1,
            total_warnings=0,
            suites=[
                {"suite": "sentiment", "status": "fail", "passed": 6, "failed": 1, "warnings": []},
            ],
        ),
        previous=_history_payload(
            benchmark_id="benchmark_previous",
            generated_at="2026-05-17T00:00:00Z",
            total_passed=7,
            total_failed=0,
            total_warnings=0,
        ),
    )
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_HISTORY_DIR", history_dir)

    response = client.get("/api/v1/benchmarks/regression")

    assert response.status_code == 200
    body = response.json()
    assert body["available"] is True
    assert body["status"] == "regression_detected"
    assert body["regression_detected"] is True
    assert "total_failed_increased" in body["reason_categories"]
    assert body["previous_total_failed"] == 0
    assert body["latest_total_failed"] == 1
    assert body["changed_suites"][0]["suite"] == "sentiment"
    assert "new_failures" in body["changed_suites"][0]["change_types"]


def test_benchmark_regression_detects_suite_pass_to_fail(monkeypatch, tmp_path) -> None:
    summary_path, history_dir = _write_latest_and_history(
        tmp_path,
        latest=_latest_payload(
            benchmark_id="benchmark_latest",
            generated_at="2026-05-17T01:00:00Z",
            total_passed=6,
            total_failed=1,
            total_warnings=0,
            suites=[
                {"suite": "topic_risk", "status": "fail", "passed": 6, "failed": 1, "warnings": []},
            ],
        ),
        previous=_history_payload(
            benchmark_id="benchmark_previous",
            generated_at="2026-05-17T00:00:00Z",
            total_passed=7,
            total_failed=0,
            total_warnings=0,
            suites=[
                {"suite": "topic_risk", "status": "pass", "passed": 7, "failed": 0, "warnings": []},
            ],
        ),
    )
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_HISTORY_DIR", history_dir)

    response = client.get("/api/v1/benchmarks/regression")

    assert response.status_code == 200
    body = response.json()
    assert body["regression_detected"] is True
    assert "suite_pass_to_fail" in body["reason_categories"]
    assert body["changed_suites"] == [
        {
            "suite": "topic_risk",
            "change_types": ["suite_pass_to_fail", "new_failures"],
            "previous_status": "pass",
            "latest_status": "fail",
            "previous_failed": 0,
            "latest_failed": 1,
            "previous_warnings": 0,
            "latest_warnings": 0,
        }
    ]


def test_benchmark_regression_malformed_latest_fails_safely(monkeypatch, tmp_path) -> None:
    summary_path = tmp_path / "offline_benchmark_summary.json"
    summary_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(benchmark_summary, "DEFAULT_BENCHMARK_SUMMARY_PATH", summary_path)

    response = client.get("/api/v1/benchmarks/regression")

    assert response.status_code == 200
    body = response.json()
    assert body["available"] is False
    assert body["status"] == "malformed"
    assert str(summary_path) not in response.text


def _latest_payload(
    *,
    benchmark_id: str,
    generated_at: str,
    total_passed: int,
    total_failed: int,
    total_warnings: int,
    suites: list[dict] | None = None,
) -> dict:
    return {
        "source": "offline_benchmark_summary",
        "benchmark_id": benchmark_id,
        "benchmark_version": "v4.0_offline_benchmark_v1",
        "generated_at": generated_at,
        "duration_seconds": 0.12,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "total_warnings": total_warnings,
        "suites": suites
        or [
            {"suite": "sentiment", "status": "pass", "passed": total_passed, "failed": 0, "warnings": []},
        ],
    }


def _history_payload(**kwargs) -> dict:
    regression_detected = kwargs.pop("regression_detected", False)
    payload = _latest_payload(**kwargs)
    payload["source"] = "offline_benchmark"
    payload["regression_detected"] = regression_detected
    return payload


def _write_latest_and_history(tmp_path, *, latest: dict, previous: dict):
    summary_path = tmp_path / "offline_benchmark_summary.json"
    summary_path.write_text(json.dumps(latest), encoding="utf-8")
    history_dir = tmp_path / "history"
    history_dir.mkdir()
    (history_dir / "previous.json").write_text(json.dumps(previous), encoding="utf-8")
    return summary_path, history_dir
