from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 10


@dataclass
class SmokeResult:
    name: str
    passed: bool
    detail: str


class SmokeClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = Request(
            url,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload) if payload else None


def run_smoke_check(base_url: str = DEFAULT_BASE_URL) -> list[SmokeResult]:
    client = SmokeClient(f"{base_url.rstrip('/')}/api/v1")
    results: list[SmokeResult] = []
    state: dict[str, Any] = {}

    def check(name: str, fn) -> None:
        try:
            detail = fn()
            results.append(SmokeResult(name=name, passed=True, detail=str(detail or "ok")))
        except Exception as exc:
            results.append(SmokeResult(name=name, passed=False, detail=str(exc)))

    check("health", lambda: _expect_key(client.request("GET", "/health"), "status"))
    check("platforms", lambda: _check_platforms(client.request("GET", "/platforms")))
    check("platform status", lambda: _expect_key(client.request("GET", "/platforms/status"), "platforms"))
    check(
        "public parser status",
        lambda: _expect_key(client.request("GET", "/public-parsers/status"), "parsers"),
    )
    check(
        "public parser preview",
        lambda: _expect_key(
            client.request(
                "POST",
                "/public-parsers/preview",
                {"platform": "hupu", "limit": 3, "use_live_fetch": False},
            ),
            "sample_posts",
        ),
    )
    check("llm status", lambda: _expect_key(client.request("GET", "/llm/status"), "provider_name"))
    check("llm usage", lambda: _expect_key(client.request("GET", "/llm/usage"), "total_calls"))
    check("benchmark latest", lambda: _expect_key(client.request("GET", "/benchmarks/latest"), "source"))
    check(
        "keyword expansion",
        lambda: _expect_key(
            client.request("POST", "/keywords/expand", {"keyword": "Tesla", "platforms": ["reddit", "weibo"]}),
            "expanded_keywords",
        ),
    )
    check(
        "crawl start",
        lambda: _expect_key(
            client.request("POST", "/crawl/start", {"keyword": "Tesla", "platforms": ["reddit", "weibo"], "limit": 20}),
            "crawl_task_id",
        ),
    )
    check(
        "analysis run",
        lambda: _expect_key(client.request("POST", "/analysis/run", {"project_id": "project_001"}), "analysis_task_id"),
    )
    check("analysis result", lambda: _expect_key(client.request("GET", "/analysis/project_001"), "risk_model_version"))
    check("list cases", lambda: len(client.request("GET", "/cases")))

    def create_case() -> str:
        case = client.request(
            "POST",
            "/cases",
            {
                "title": "Smoke Test Case",
                "keyword": "Tesla",
                "platforms": ["reddit", "weibo", "bilibili"],
                "report_language": "zh-CN",
            },
        )
        case_id = _expect_key(case, "case_id")
        state["case_id"] = case_id
        return case_id

    check("create case", create_case)

    def run_case() -> str:
        case = client.request("POST", f"/cases/{state['case_id']}/run")
        assert case.get("status") == "completed", "case did not complete"
        assert case.get("markdown_available") is True, "markdown not available after run"
        state["project_id"] = case["project_id"]
        return case["status"]

    check("run case", run_case)
    check("case detail", lambda: _expect_key(client.request("GET", f"/cases/{state['case_id']}"), "report"))
    check("case snapshots", lambda: _expect_min_len(client.request("GET", f"/cases/{state['case_id']}/snapshots"), 1))
    check(
        "markdown export",
        lambda: _check_markdown(client.request("GET", f"/cases/{state['case_id']}/report/markdown")),
    )
    check(
        "visualization data",
        lambda: _expect_key(
            client.request("POST", "/visualization/data", {"project_id": state["project_id"]}),
            "topic_risks",
        ),
    )
    check(
        "summary report",
        lambda: _expect_report(client.request("POST", "/summary/generate", {"project_id": state["project_id"], "report_language": "zh-CN"})),
    )
    check(
        "recommendation report",
        lambda: _expect_report(
            client.request("POST", "/recommendation/generate", {"project_id": state["project_id"], "report_language": "zh-CN"})
        ),
    )

    def monitor_run() -> int:
        status = client.request("POST", f"/cases/{state['case_id']}/monitor/run")
        alerts = status.get("alerts") or []
        state["monitor_alert_count"] = len(alerts)
        return len(alerts)

    check("monitor run", monitor_run)
    check("forecast", lambda: _expect_key(client.request("GET", f"/cases/{state['case_id']}/forecast"), "forecast_status"))
    check(
        "forecast run",
        lambda: _expect_key(client.request("POST", f"/cases/{state['case_id']}/forecast/run"), "predicted_risk_score"),
    )
    check("case alerts", lambda: _expect_min_len(client.request("GET", f"/cases/{state['case_id']}/alerts"), 1))
    check("global alerts", lambda: _expect_min_len(client.request("GET", "/alerts"), 1))
    check("scheduler status", lambda: _expect_key(client.request("GET", "/scheduler/status"), "background_scheduler_running"))
    check("enable monitoring", lambda: _expect_key(client.request("POST", f"/cases/{state['case_id']}/monitoring/enable"), "enabled"))
    check("scheduler run due", lambda: _expect_key(client.request("POST", "/scheduler/run-due"), "executed_case_count"))

    def list_notifications() -> str:
        notifications = client.request("GET", f"/cases/{state['case_id']}/notifications")
        _expect_min_len(notifications, 1)
        notification = notifications[0]
        for field in ("notification_id", "alert_id", "case_id", "level", "title", "message", "status", "created_at"):
            assert field in notification, f"notification missing {field}"
        state["notification_id"] = notification["notification_id"]
        return notification["notification_id"]

    check("case notifications", list_notifications)
    check("global notifications", lambda: _expect_min_len(client.request("GET", "/notifications"), 1))
    check("outbox status", lambda: _expect_key(client.request("GET", "/notifications/outbox/status"), "total"))
    check(
        "mark notification read",
        lambda: _expect_key(client.request("POST", f"/notifications/{state['notification_id']}/read"), "read_at"),
    )
    check(
        "simulate send notification",
        lambda: _expect_key(
            client.request("POST", f"/notifications/{state['notification_id']}/simulate-send"),
            "simulated_sent_at",
        ),
    )
    check("simulate send pending", lambda: len(client.request("POST", "/notifications/simulate-send-pending")))

    def simulation_run() -> str:
        scenario = client.request("GET", "/simulation/demo-scenario")
        _expect_key(scenario, "scenario_id")
        state["simulation_scenario"] = scenario
        result = client.request("POST", "/simulation/run", scenario)
        _expect_key(result, "simulation_status")
        state["simulation_run_result"] = result
        return result["simulation_status"]

    check("simulation demo scenario", lambda: _expect_key(client.request("GET", "/simulation/demo-scenario"), "scenario_id"))
    check("simulation run", simulation_run)

    def simulation_report_export() -> str:
        report = client.request(
            "POST",
            "/simulation/report/markdown",
            {
                "simulation_mode": "single",
                "scenario_name": state["simulation_run_result"].get("scenario_name", "Smoke demo scenario"),
                "intervention_a": "clarification",
                "run_result": state["simulation_run_result"],
                "generated_from": "api_smoke_check",
            },
        )
        markdown = _expect_key(report, "markdown")
        for section in (
            "# Simulation Lab Strategy Report",
            "## Scenario Overview",
            "## Ethical Risk Review",
            "## Recommended Human Review Questions",
            "## Limitations",
        ):
            assert section in markdown, f"simulation report missing {section}"
        return "markdown ok"

    check("simulation report export", simulation_report_export)

    return results


def _expect_key(payload: Any, key: str) -> Any:
    assert isinstance(payload, dict), f"expected object with key {key}"
    assert key in payload, f"missing key {key}"
    return payload[key]


def _expect_min_len(payload: Any, minimum: int) -> int:
    assert isinstance(payload, list), "expected list response"
    assert len(payload) >= minimum, f"expected at least {minimum} item(s), got {len(payload)}"
    return len(payload)


def _check_platforms(payload: Any) -> str:
    platforms = _expect_key(payload, "platforms")
    active = _expect_key(payload, "active_mvp_platforms")
    assert "reddit" in active, "reddit should remain mock-selectable"
    assert "youtube" not in active, "youtube must not be active in MVP"
    return f"{len(platforms)} platforms, {len(active)} active mock platforms"


def _check_markdown(payload: Any) -> str:
    markdown = _expect_key(payload, "markdown")
    for text in ("# ", "risk", "v1_5_topic_risk_mvp"):
        assert text in markdown, f"markdown missing {text}"
    return "markdown ok"


def _expect_report(payload: Any) -> str:
    assert payload.get("report_language") == "zh-CN", "report language should be zh-CN"
    for key in ("overall_summary", "recommended_actions", "suggested_public_response", "risk_model_version"):
        assert key in payload, f"report missing {key}"
    return payload["risk_model_version"]


def print_summary(results: list[SmokeResult]) -> None:
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    print(f"\nSummary: {passed} passed, {failed} failed")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run local Sentigraph API smoke checks.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Backend base URL, without /api/v1.")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    results = run_smoke_check(args.base_url)
    print_summary(results)
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
