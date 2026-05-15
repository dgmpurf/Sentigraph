from __future__ import annotations

from app.core.environment import PROJECT_ENV_PATH, REPOSITORY_ROOT, reddit_env_diagnostics


def test_project_env_path_points_to_repository_root() -> None:
    assert PROJECT_ENV_PATH == REPOSITORY_ROOT / ".env"
    assert (REPOSITORY_ROOT / "AGENTS.md").exists()
    assert (REPOSITORY_ROOT / "backend").exists()


def test_gitignore_excludes_project_env_file() -> None:
    gitignore = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert ".env" in {line.strip() for line in gitignore}


def test_reddit_env_diagnostics_reports_presence_without_secret_values(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")
    monkeypatch.setenv("REDDIT_CLIENT_ID", "client-id-should-not-appear")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "client-secret-should-not-appear")
    monkeypatch.setenv("REDDIT_USER_AGENT", "sentigraph-test-agent")

    diagnostics = reddit_env_diagnostics()

    assert diagnostics == {
        "REDDIT_ADAPTER_MODE": "real",
        "REDDIT_CLIENT_ID": "present",
        "REDDIT_CLIENT_SECRET": "present",
        "REDDIT_USER_AGENT": "present",
    }
    serialized = str(diagnostics)
    assert "client-id-should-not-appear" not in serialized
    assert "client-secret-should-not-appear" not in serialized
    assert "sentigraph-test-agent" not in serialized


def test_reddit_env_diagnostics_reports_missing_credentials(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "mock")
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)

    diagnostics = reddit_env_diagnostics()

    assert diagnostics["REDDIT_ADAPTER_MODE"] == "mock"
    assert diagnostics["REDDIT_CLIENT_ID"] == "missing"
    assert diagnostics["REDDIT_CLIENT_SECRET"] == "missing"
    assert diagnostics["REDDIT_USER_AGENT"] == "missing"
