"""Windows-host synthetic concurrency tests of the real LocalJson store."""

from __future__ import annotations

import json
import multiprocessing
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseCreateRequest, MarkdownExportResponse
from app.services.storage.base_store import CaseRevisionConflict
from app.services.storage import local_json_store as local_module
from app.services.storage.local_json_store import LocalJsonCaseStore


TIMEOUT = 15.0


def _receive(conn):
    assert conn.poll(TIMEOUT), "task-owned child did not respond"
    return conn.recv()


def _stop_child(process) -> None:
    process.join(TIMEOUT)
    if process.is_alive():
        process.terminate()
        process.join(TIMEOUT)
    assert not process.is_alive()


def _cas_worker(path: str, marker: str, start, conn) -> None:
    store = LocalJsonCaseStore(path)
    case = store.get_case("case_001")
    conn.send(("ready", case.case_revision))
    if not start.wait(TIMEOUT):
        conn.send(("timeout", None))
        return
    candidate = case.model_copy(update={"title": marker}, deep=True)
    try:
        saved = store.replace_case_if_revision_matches(candidate, 0)
        conn.send(("winner", saved.case_revision, marker))
    except CaseRevisionConflict as exc:
        conn.send(("conflict", exc.current_revision, marker))


def _hold_lock_worker(path: str, conn) -> None:
    store = LocalJsonCaseStore(path)
    with store._write_transaction():
        conn.send(("entered", os.getpid()))
        conn.recv()  # Parent terminates this process while it owns the composition.


def _hold_lock_once_worker(path: str, conn) -> None:
    store = LocalJsonCaseStore(path)
    with store._write_transaction():
        conn.send(("entered", os.getpid()))


def _aux_worker(path: str, start, conn) -> None:
    store = LocalJsonCaseStore(path)
    report = MarkdownExportResponse(
        case_id="case_001",
        project_id="project_001",
        filename="synthetic.md",
        markdown="# Synthetic",
        generated_at=datetime(2026, 5, 14, tzinfo=timezone.utc),
    )
    conn.send(("ready", None))
    if not start.wait(TIMEOUT):
        conn.send(("timeout", None))
        return
    store.save_markdown_report("case_001", report)
    conn.send(("appended", None))


def _created_store(tmp_path):
    path = tmp_path / "cases.json"
    store = LocalJsonCaseStore(path)
    CaseRepository(store).create_case(AnalysisCaseCreateRequest(keyword="synthetic"))
    return store, path


@pytest.mark.skipif(os.name != "nt", reason="F1R3 same-host proof target is Windows")
def test_same_path_registry_and_two_thread_composition(monkeypatch, tmp_path) -> None:
    first, path = _created_store(tmp_path)
    second = LocalJsonCaseStore(Path(str(tmp_path) + "\\.\\cases.json"))
    case_variant = LocalJsonCaseStore(Path(str(path).swapcase()))
    other = LocalJsonCaseStore(tmp_path / "other_cases.json")
    assert first._lock is second._lock is case_variant._lock
    assert other._lock is not first._lock

    holder_entered = threading.Event()
    release_holder = threading.Event()
    contender_attempted = threading.Event()
    contender_os_attempted = threading.Event()
    contender_entered = threading.Event()
    errors = []
    original_lock_fd = local_module._lock_file_descriptor

    def observed_lock_fd(fd):
        if threading.current_thread().name == "contender":
            contender_os_attempted.set()
        return original_lock_fd(fd)

    monkeypatch.setattr(local_module, "_lock_file_descriptor", observed_lock_fd)

    def holder() -> None:
        try:
            with first._write_transaction():
                holder_entered.set()
                assert release_holder.wait(TIMEOUT)
        except BaseException as exc:
            errors.append(exc)
            holder_entered.set()

    def contender() -> None:
        try:
            contender_attempted.set()
            with second._write_transaction():
                contender_entered.set()
        except BaseException as exc:
            errors.append(exc)

    holder_thread = threading.Thread(target=holder, name="holder")
    contender_thread = threading.Thread(target=contender, name="contender")
    try:
        holder_thread.start()
        assert holder_entered.wait(TIMEOUT) and not errors
        contender_thread.start()
        assert contender_attempted.wait(TIMEOUT)
        assert not contender_os_attempted.wait(0.2)
        assert not contender_entered.is_set()
    finally:
        release_holder.set()
        if holder_thread.ident is not None:
            holder_thread.join(TIMEOUT)
        if contender_thread.ident is not None:
            contender_thread.join(TIMEOUT)
    assert not errors
    assert not holder_thread.is_alive() and not contender_thread.is_alive()
    assert contender_os_attempted.is_set() and contender_entered.is_set()


@pytest.mark.skipif(os.name != "nt", reason="F1R3 same-host proof target is Windows")
def test_two_processes_one_cas_winner_and_one_conflict(tmp_path) -> None:
    store, path = _created_store(tmp_path)
    context = multiprocessing.get_context("spawn")
    start = context.Event()
    children = []
    conns = []
    try:
        for marker in ("candidate_a", "candidate_b"):
            parent, child = context.Pipe(duplex=True)
            process = context.Process(target=_cas_worker, args=(str(path), marker, start, child))
            process.start()
            child.close()
            children.append(process)
            conns.append(parent)
        assert [_receive(conn) for conn in conns] == [("ready", 0), ("ready", 0)]
        start.set()
        outcomes = [_receive(conn) for conn in conns]
    finally:
        start.set()
        for process in children:
            _stop_child(process)
        for conn in conns:
            conn.close()
    assert sorted(outcome[0] for outcome in outcomes) == ["conflict", "winner"]
    assert all(outcome[1] == 1 for outcome in outcomes)
    winner_marker = next(outcome[2] for outcome in outcomes if outcome[0] == "winner")
    persisted = store.get_case("case_001")
    assert persisted.case_revision == 1
    assert persisted.title == winner_marker
    assert json.loads(path.read_text(encoding="utf-8"))["cases"]["case_001"]["case_revision"] == 1


@pytest.mark.skipif(os.name != "nt", reason="F1R3 same-host proof target is Windows")
def test_process_death_releases_actual_composed_lock(tmp_path) -> None:
    _store, path = _created_store(tmp_path)
    context = multiprocessing.get_context("spawn")
    first_parent, first_child = context.Pipe(duplex=True)
    holder = context.Process(target=_hold_lock_worker, args=(str(path), first_child))
    holder.start()
    first_child.close()
    try:
        first_status = _receive(first_parent)
        assert first_status[0] == "entered"
        holder.terminate()
        _stop_child(holder)
        lock_path = path.with_name(path.name + ".lock")
        assert lock_path.exists() and lock_path.stat().st_size >= 1
        fresh_parent, fresh_child = context.Pipe(duplex=True)
        fresh = context.Process(target=_hold_lock_once_worker, args=(str(path), fresh_child))
        fresh.start()
        fresh_child.close()
        try:
            fresh_status = _receive(fresh_parent)
            assert fresh_status[0] == "entered" and fresh_status[1] != first_status[1]
        finally:
            _stop_child(fresh)
            fresh_parent.close()
        assert lock_path.exists() and lock_path.stat().st_size >= 1
    finally:
        if holder.is_alive():
            holder.terminate()
        _stop_child(holder)
        first_parent.close()


@pytest.mark.skipif(os.name != "nt", reason="F1R3 same-host proof target is Windows")
def test_auxiliary_writer_does_not_clobber_cas_winner(tmp_path) -> None:
    store, path = _created_store(tmp_path)
    context = multiprocessing.get_context("spawn")
    start = context.Event()
    case_parent, case_child = context.Pipe(duplex=True)
    aux_parent, aux_child = context.Pipe(duplex=True)
    case_process = context.Process(target=_cas_worker, args=(str(path), "case_winner", start, case_child))
    aux_process = context.Process(target=_aux_worker, args=(str(path), start, aux_child))
    case_process.start()
    aux_process.start()
    case_child.close()
    aux_child.close()
    try:
        assert _receive(case_parent) == ("ready", 0)
        assert _receive(aux_parent) == ("ready", None)
        start.set()
        assert _receive(case_parent) == ("winner", 1, "case_winner")
        assert _receive(aux_parent) == ("appended", None)
    finally:
        start.set()
        _stop_child(case_process)
        _stop_child(aux_process)
        case_parent.close()
        aux_parent.close()
    assert store.get_case("case_001").title == "case_winner"
    assert store.get_case("case_001").case_revision == 1
    assert store.get_markdown_report("case_001").markdown == "# Synthetic"


def test_unique_pid_temp_names_and_strict_canonical_json(monkeypatch, tmp_path) -> None:
    path = tmp_path / "cases.json"
    captured = []
    original_replace = local_module.os.replace

    def observed_replace(src, dst):
        captured.append((Path(src).name, Path(dst).name))
        return original_replace(src, dst)

    monkeypatch.setattr(local_module.os, "replace", observed_replace)
    store = LocalJsonCaseStore(path)
    created = CaseRepository(store).create_case(AnalysisCaseCreateRequest(keyword="temp"))
    store.update_case(created.model_copy(update={"title": "updated"}, deep=True))
    assert len(captured) == 2
    assert len({source for source, _target in captured}) == 2
    assert all(re.fullmatch(rf"cases\.json\.{os.getpid()}\.[0-9a-f]{{32}}\.tmp", source)
               for source, _target in captured)
    assert all(target == "cases.json" for _source, target in captured)
    assert list(tmp_path.glob("*.tmp")) == []
    parsed = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    assert parsed["cases"][created.case_id]["title"] == "updated"
