"""Synthetic, repository-local tests for the case revision CAS contract."""

import json

import pytest

from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseCreateRequest
from app.services.storage.base_store import CaseRevisionConflict
from app.services.storage.local_json_store import LocalJsonCaseStore


def _repository(tmp_path):
    path = tmp_path / "cases.json"
    store = LocalJsonCaseStore(path)
    return CaseRepository(store), path


def test_new_case_revision_zero_then_two_conditional_winners(tmp_path) -> None:
    repository, path = _repository(tmp_path)
    created = repository.create_case(AnalysisCaseCreateRequest(keyword="synthetic"))
    assert created.case_revision == 0
    assert repository.get_case(created.case_id).case_revision == 0
    assert repository.list_cases()[0].case_revision == 0

    stale = created.model_copy(update={"title": "stale contender"}, deep=True)
    first = repository.replace_case_if_revision_matches(
        created.model_copy(update={"title": "first winner"}, deep=True), 0
    )
    assert first is not None
    assert first.case_revision == 1
    assert repository.get_case(created.case_id).title == "first winner"
    assert repository.list_cases()[0].case_revision == 1

    before_conflict = path.read_bytes()
    with pytest.raises(CaseRevisionConflict) as error:
        repository.replace_case_if_revision_matches(stale, 0)
    assert error.value.case_id == created.case_id
    assert error.value.expected_revision == 0
    assert error.value.current_revision == 1
    assert path.read_bytes() == before_conflict

    second = repository.replace_case_if_revision_matches(
        first.model_copy(update={"title": "second winner"}, deep=True), 1
    )
    assert second is not None
    assert second.case_revision == 2
    assert repository.get_case(created.case_id).case_revision == 2
    assert repository.list_cases()[0].case_revision == 2
    assert repository.get_case(created.case_id).title == "second winner"
    second.title = "detached only"
    assert repository.get_case(created.case_id).title == "second winner"


def test_legacy_missing_revision_is_logical_zero_and_missing_case_is_distinct(tmp_path) -> None:
    repository, path = _repository(tmp_path)
    created = repository.create_case(AnalysisCaseCreateRequest(keyword="legacy"))
    data = json.loads(path.read_text(encoding="utf-8"))
    del data["cases"][created.case_id]["case_revision"]
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    legacy = repository.get_case(created.case_id)
    assert legacy is not None
    assert legacy.case_revision == 0
    saved = repository.replace_case_if_revision_matches(legacy, 0)
    assert saved is not None and saved.case_revision == 1
    assert json.loads(path.read_text(encoding="utf-8"))["cases"][created.case_id]["case_revision"] == 1

    missing = saved.model_copy(update={"case_id": "case_missing", "case_revision": 1}, deep=True)
    assert repository.replace_case_if_revision_matches(missing, 1) is None


@pytest.mark.parametrize("expected", [True, -1, 1])
def test_invalid_revision_precondition_has_no_case_write(tmp_path, expected) -> None:
    repository, path = _repository(tmp_path)
    created = repository.create_case(AnalysisCaseCreateRequest(keyword="guard"))
    before = path.read_bytes()
    with pytest.raises(ValueError):
        repository.replace_case_if_revision_matches(created, expected)
    assert path.read_bytes() == before


def test_repository_forwards_original_expected_revision(monkeypatch, tmp_path) -> None:
    repository, _path = _repository(tmp_path)
    created = repository.create_case(AnalysisCaseCreateRequest(keyword="forward"))
    captured = []

    def spy(case, expected_revision):
        captured.append((case, expected_revision))
        return None

    monkeypatch.setattr(repository.store, "replace_case_if_revision_matches", spy)
    assert repository.replace_case_if_revision_matches(created, 0) is None
    assert captured == [(created, 0)]
