from __future__ import annotations

import pytest

from sentigraph_shared.json_framing import (
    DuplicateKeyPolicy,
    JsonFramingError,
    JsonFramingType,
    JsonInputDescriptor,
    JsonRootShape,
    parse_jsonl_records,
    parse_single_json_document,
    serialize_single_json_document,
)


SOURCE_ROLE = "test_json_input"
CONTAINER_ROLE = "test_container"
MEMBER_ROLE = "test.json"


def _descriptor(
    data: bytes,
    *,
    framing_type: JsonFramingType = JsonFramingType.SINGLE_JSON,
    root_shape: JsonRootShape = JsonRootShape.OBJECT_ONLY,
    source_role: str = SOURCE_ROLE,
    container_role: str = CONTAINER_ROLE,
    member_role: str = MEMBER_ROLE,
) -> JsonInputDescriptor:
    return JsonInputDescriptor.from_bytes(
        data,
        source_role=source_role,
        framing_type=framing_type,
        encoding="utf-8",
        container_role=container_role,
        member_role=member_role,
        root_shape=root_shape,
        duplicate_key_policy=DuplicateKeyPolicy.REJECT_DUPLICATE_KEYS,
    )


def _parse_single(data: bytes, descriptor: JsonInputDescriptor):
    return parse_single_json_document(
        data,
        descriptor,
        expected_source_role=SOURCE_ROLE,
        expected_container_role=CONTAINER_ROLE,
        expected_member_role=MEMBER_ROLE,
    )


def _parse_jsonl(data: bytes, descriptor: JsonInputDescriptor):
    return parse_jsonl_records(
        data,
        descriptor,
        expected_source_role=SOURCE_ROLE,
        expected_container_role=CONTAINER_ROLE,
        expected_member_role=MEMBER_ROLE,
        allow_blank_lines=True,
    )


def test_valid_object() -> None:
    data = b'{"value":1}'
    assert _parse_single(data, _descriptor(data)) == {"value": 1}


def test_valid_array() -> None:
    data = b"[1,2]"
    assert _parse_single(data, _descriptor(data, root_shape=JsonRootShape.ARRAY_ONLY)) == [1, 2]


def test_valid_with_trailing_whitespace() -> None:
    data = b'{"value":1}\r\n\t '
    assert _parse_single(data, _descriptor(data)) == {"value": 1}


@pytest.mark.parametrize(
    ("data", "reason_code"),
    [
        (b'{"value":1} trailer', "TRAILING_NONWHITESPACE"),
        (b'{"value":1}{"next":2}', "TRAILING_NONWHITESPACE"),
    ],
)
def test_nonwhitespace_trailer_and_concatenated_objects_reject(data: bytes, reason_code: str) -> None:
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, _descriptor(data))
    assert captured.value.reason_code == reason_code


def test_jsonl_two_documents_and_blank_line_policy() -> None:
    data = b'{"row":1}\n\n{"row":2}\n'
    descriptor = _descriptor(data, framing_type=JsonFramingType.JSONL)
    assert _parse_jsonl(data, descriptor) == [{"row": 1}, {"row": 2}]


def test_malformed_jsonl_line_has_bounded_line_number() -> None:
    data = b'{"row":1}\n{"row":}\n'
    descriptor = _descriptor(data, framing_type=JsonFramingType.JSONL)
    with pytest.raises(JsonFramingError) as captured:
        _parse_jsonl(data, descriptor)
    assert captured.value.reason_code == "JSONL_RECORD_DECODE_FAILED"
    assert captured.value.line_number == 2
    assert "{\"row\":" not in str(captured.value.as_dict())


def test_wrong_retained_role_rejects_before_invalid_json_parse() -> None:
    data = b"not-json"
    descriptor = _descriptor(data, source_role="wrong_source_role")
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, descriptor)
    assert captured.value.reason_code == "SOURCE_ROLE_MISMATCH"


def test_wrong_archive_member_rejects_before_parse() -> None:
    data = b'{"value":1}'
    descriptor = _descriptor(data, member_role="wrong.json")
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, descriptor)
    assert captured.value.reason_code == "MEMBER_ROLE_MISMATCH"


def test_bytes_decode_or_slice_truncation_rejects() -> None:
    data = '{"value":"中'.encode("utf-8")[:-1]
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, _descriptor(data))
    assert captured.value.reason_code == "DECODE_FAILED"


def test_extra_data_style_negative_regression_shape_is_forward_only() -> None:
    first = '{"value":"' + ("x" * 789) + '"}'
    assert len(first) == 801
    data = (first + '{"next":1}').encode("utf-8")
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, _descriptor(data))
    assert captured.value.reason_code == "TRAILING_NONWHITESPACE"
    assert captured.value.offset == 801
    fixture_metadata = {"historical_reproduction": False, "historical_cause_claim": False}
    assert fixture_metadata == {"historical_reproduction": False, "historical_cause_claim": False}


def test_duplicate_object_key_single_json_rejects() -> None:
    data = b'{"value":1,"value":2}'
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, _descriptor(data))
    assert captured.value.reason_code == "DUPLICATE_OBJECT_KEY"


def test_duplicate_object_key_jsonl_record_rejects_with_line() -> None:
    data = b'{"row":1}\n{"row":2,"row":3}\n'
    descriptor = _descriptor(data, framing_type=JsonFramingType.JSONL)
    with pytest.raises(JsonFramingError) as captured:
        _parse_jsonl(data, descriptor)
    assert captured.value.reason_code == "DUPLICATE_OBJECT_KEY"
    assert captured.value.line_number == 2


@pytest.mark.parametrize(
    ("data", "root_shape", "reason_code"),
    [
        (b"[]", JsonRootShape.OBJECT_ONLY, "ROOT_SHAPE_OBJECT_REQUIRED"),
        (b"{}", JsonRootShape.ARRAY_ONLY, "ROOT_SHAPE_ARRAY_REQUIRED"),
    ],
)
def test_root_shape_mismatch_rejects(data: bytes, root_shape: JsonRootShape, reason_code: str) -> None:
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, _descriptor(data, root_shape=root_shape))
    assert captured.value.reason_code == reason_code


def test_any_json_value_scalar_accepts_only_when_declared() -> None:
    data = b"7"
    assert _parse_single(data, _descriptor(data, root_shape=JsonRootShape.ANY_JSON_VALUE)) == 7
    with pytest.raises(JsonFramingError):
        _parse_single(data, _descriptor(data, root_shape=JsonRootShape.OBJECT_ONLY))


def test_explicit_container_is_not_routed_to_single_document_parser() -> None:
    data = b'{"value":1}'
    descriptor = _descriptor(data, framing_type=JsonFramingType.EXPLICIT_CONTAINER)
    with pytest.raises(JsonFramingError) as captured:
        _parse_single(data, descriptor)
    assert captured.value.reason_code == "FRAMING_TYPE_MISMATCH"


def test_serialize_single_document_once_returns_bound_descriptor() -> None:
    data, descriptor = serialize_single_json_document(
        {"value": "中"},
        source_role=SOURCE_ROLE,
        encoding="utf-8",
        container_role=CONTAINER_ROLE,
        member_role=MEMBER_ROLE,
        root_shape=JsonRootShape.OBJECT_ONLY,
    )
    assert data == '{"value":"中"}'.encode("utf-8")
    assert descriptor.byte_length == len(data)
    assert _parse_single(data, descriptor) == {"value": "中"}
