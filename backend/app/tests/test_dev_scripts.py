from __future__ import annotations

import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def test_reset_local_data_only_deletes_runtime_json(tmp_path) -> None:
    script = _load_script("reset_local_data.py")
    data_dir = tmp_path / "backend" / "data"
    data_dir.mkdir(parents=True)
    gitkeep = data_dir / ".gitkeep"
    gitkeep.write_text("\n", encoding="utf-8")
    source_like = data_dir / "keep.txt"
    source_like.write_text("do not delete", encoding="utf-8")
    runtime = data_dir / "cases.json"
    runtime.write_text("{}", encoding="utf-8")
    runtime_tmp = data_dir / "cases.json.tmp"
    runtime_tmp.write_text("{}", encoding="utf-8")

    dry_run = script.reset_local_data(repo_root=tmp_path, yes=False)
    result = script.reset_local_data(repo_root=tmp_path, yes=True)

    assert dry_run["dry_run"] is True
    assert len(dry_run["would_delete"]) == 2
    assert len(result["deleted"]) == 2
    assert not runtime.exists()
    assert not runtime_tmp.exists()
    assert gitkeep.exists()
    assert source_like.exists()


def test_seed_demo_cases_creates_complete_notification_ready_store(tmp_path) -> None:
    script = _load_script("seed_demo_cases.py")
    store_path = tmp_path / "cases.json"

    result = script.seed_demo_cases(store_path=store_path, reset_first=True)
    data = json.loads(store_path.read_text(encoding="utf-8"))

    assert result["mock_only"] is True
    assert result["case_count"] >= 3
    assert result["snapshot_count"] >= 3
    assert result["alert_count"] >= 1
    assert result["notification_count"] >= 1
    assert result["forecast_status"] == "ready"
    assert result["simulation_initialization_status"] == "initialized"
    assert result["simulation_sub_issue_count"] >= 1
    assert result["simulation_audience_segment_count"] >= 1
    assert result["completed_case_id"] in data["cases"]
    assert result["public_parser_case_id"] in data["cases"]
    assert result["public_parser_preview_platform"] == "hupu"
    assert result["public_parser_preview_post_count"] >= 1
    assert result["public_parser_preview_comment_count"] >= 1
    assert data["cases"][result["completed_case_id"]]["status"] == "completed"
    assert data["markdown_reports"][result["completed_case_id"]]["markdown"]
    assert data["notifications"]


def _load_script(filename: str):
    path = SCRIPTS_DIR / filename
    spec = importlib.util.spec_from_file_location(filename.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module
