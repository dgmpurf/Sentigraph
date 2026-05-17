from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
DEFAULT_STORE_PATH = REPO_ROOT / "backend" / "data" / "cases.json"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseCreateRequest
from app.services.case_store import (
    configure_case_repository,
    create_case,
    get_case_repository,
    run_case,
    run_monitoring_check,
)
from app.services.crawling.public_parser.parser_status_service import preview_public_parser
from app.services.monitoring.scheduler_service import enable_case_monitoring, run_due_monitoring_jobs
from app.services.storage.local_json_store import LocalJsonCaseStore


def seed_demo_cases(
    *,
    store_path: str | Path | None = None,
    reset_first: bool = False,
) -> dict[str, Any]:
    """Create deterministic local demo cases without external services."""

    if store_path is not None:
        configure_case_repository(CaseRepository(LocalJsonCaseStore(store_path)))

    repository = get_case_repository()
    if reset_first:
        repository.reset()

    primary = create_case(
        AnalysisCaseCreateRequest(
            title="Tesla Demo Case",
            keyword="Tesla",
            platforms=["reddit", "weibo", "bilibili"],
            report_language="zh-CN",
        )
    )
    completed = run_case(primary.case_id)
    if completed is None:
        raise RuntimeError("Failed to run primary demo case.")

    # Two manual checks make the demo useful: one trend increase and one richer alert set.
    run_monitoring_check(completed.case_id)
    run_monitoring_check(completed.case_id)

    enable_case_monitoring(completed.case_id)
    scheduler_result = run_due_monitoring_jobs()

    secondary = create_case(
        AnalysisCaseCreateRequest(
            title="BYD Draft Watch",
            keyword="BYD",
            platforms=["weibo", "douyin", "xiaohongshu"],
            report_language="zh-CN",
        )
    )

    public_parser_case = create_case(
        AnalysisCaseCreateRequest(
            title="Hupu Fixture Parser Watch",
            keyword="hupu_fixture_public_discussion",
            platforms=["hupu"],
            report_language="zh-CN",
        )
    )
    public_parser_completed = run_case(public_parser_case.case_id)
    if public_parser_completed is None:
        raise RuntimeError("Failed to run public parser demo case.")
    public_parser_preview = preview_public_parser("hupu", limit=3, use_live_fetch=False)

    snapshots = repository.list_analysis_snapshots(completed.case_id)
    alerts = repository.list_case_alerts(completed.case_id)
    notifications = repository.list_case_notifications(completed.case_id)
    cases = repository.list_cases()

    return {
        "store_path": str(getattr(repository.store, "path", DEFAULT_STORE_PATH)),
        "created_case_ids": [primary.case_id, secondary.case_id, public_parser_case.case_id],
        "completed_case_id": completed.case_id,
        "public_parser_case_id": public_parser_completed.case_id,
        "public_parser_preview_platform": public_parser_preview.platform,
        "public_parser_preview_post_count": public_parser_preview.post_count,
        "public_parser_preview_comment_count": public_parser_preview.comment_count,
        "case_count": len(cases),
        "snapshot_count": len(snapshots),
        "alert_count": len(alerts),
        "notification_count": len(notifications),
        "scheduler_executed_case_count": scheduler_result.executed_case_count,
        "mock_only": True,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Seed deterministic Sentigraph local demo cases using the offline mock pipeline."
    )
    parser.add_argument(
        "--store-path",
        default=str(DEFAULT_STORE_PATH),
        help="Project-local JSON store path. Defaults to backend/data/cases.json.",
    )
    parser.add_argument(
        "--reset-first",
        action="store_true",
        help="Reset the selected local JSON store before seeding demo data.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    result = seed_demo_cases(store_path=args.store_path, reset_first=args.reset_first)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
