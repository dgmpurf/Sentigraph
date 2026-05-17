from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def test_offline_benchmark_runner_passes_without_server_or_external_calls() -> None:
    script = _load_script("run_offline_benchmarks.py")

    result = script.run_all_benchmarks(write_json=False)

    assert result["benchmark_version"] == "v4.0_offline_benchmark_v1"
    assert result["total_failed"] == 0
    assert result["safe_mode"] == {
        "real_llm_calls": False,
        "real_platform_calls": False,
        "live_fetch_enabled": False,
        "backend_server_required": False,
        "api_keys_required": False,
    }
    assert {suite["suite"] for suite in result["suites"]} == {
        "sentiment",
        "topic_cluster",
        "topic_risk",
        "report_builder",
        "markdown_export",
        "selector_repair",
        "public_parser_fixtures",
        "platform_adapter_mocks",
    }


def test_offline_benchmark_runner_can_write_safe_json_summary(tmp_path) -> None:
    script = _load_script("run_offline_benchmarks.py")

    result = script.run_all_benchmarks(output_dir=tmp_path, write_json=True)
    summary_path = Path(result["json_summary_path"])
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary_path.parent == tmp_path
    assert summary["total_failed"] == 0
    summary_text = summary_path.read_text(encoding="utf-8").lower()
    assert "raw prompt" not in summary_text
    assert "openai_api_key" not in summary_text
    assert "deepseek_api_key" not in summary_text
    assert "qwen_api_key" not in summary_text


def test_offline_benchmark_runner_reports_missing_fixture_safely(tmp_path) -> None:
    script = _load_script("run_offline_benchmarks.py")
    fixture_dir = tmp_path / "benchmarks"
    shutil.copytree(REPO_ROOT / "benchmarks", fixture_dir)
    (fixture_dir / "sentiment_cases.json").unlink()

    result = script.run_all_benchmarks(fixture_dir=fixture_dir, write_json=False)
    sentiment_suite = next(suite for suite in result["suites"] if suite["suite"] == "sentiment")

    assert result["total_failed"] >= 1
    assert sentiment_suite["status"] == "fail"
    assert sentiment_suite["cases"][0]["details"]["error_category"] == "fixture_error"
    assert "sentiment_cases.json" in sentiment_suite["cases"][0]["message"]


def _load_script(filename: str):
    path = SCRIPTS_DIR / filename
    spec = importlib.util.spec_from_file_location(filename.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module
