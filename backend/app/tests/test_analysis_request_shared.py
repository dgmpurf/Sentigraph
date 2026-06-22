from __future__ import annotations

import inspect
import re

from app.services import analysis_request_shared


def test_utc_compact_timestamp_preserves_existing_shape() -> None:
    value = analysis_request_shared.utc_compact_timestamp()

    assert re.fullmatch(r"\d{8}T\d{6}Z", value)


def test_generate_record_id_preserves_existing_prefixed_shape() -> None:
    value = analysis_request_shared.generate_record_id("report_export_public_access_external_delivery_gate")

    assert re.fullmatch(r"report_export_public_access_external_delivery_gate_\d{8}T\d{6}Z_[0-9a-f]{8}", value)


def test_generate_record_id_rejects_blank_prefix() -> None:
    try:
        analysis_request_shared.generate_record_id(" ")
    except ValueError as exc:
        assert "prefix" in str(exc).lower()
    else:
        raise AssertionError("blank prefixes should not produce record ids")


def test_shared_id_helper_does_not_touch_runtime_files_or_network() -> None:
    source = inspect.getsource(analysis_request_shared)

    forbidden_tokens = [
        "open(",
        "read_text(",
        "read_bytes(",
        "write_text(",
        "write_bytes(",
        "requests.",
        "httpx",
        "urllib",
        "subprocess",
        "os.environ",
        "Path(",
    ]
    for token in forbidden_tokens:
        assert token not in source

