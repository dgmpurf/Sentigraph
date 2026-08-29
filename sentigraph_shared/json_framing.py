"""Canonical JSON framing and provenance helpers for governed Sentigraph inputs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from typing import Any


_SAFE_ROLE_RE = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class JsonFramingType(str, Enum):
    SINGLE_JSON = "SINGLE_JSON"
    JSONL = "JSONL"
    EXPLICIT_CONTAINER = "EXPLICIT_CONTAINER"


class JsonRootShape(str, Enum):
    OBJECT_ONLY = "OBJECT_ONLY"
    ARRAY_ONLY = "ARRAY_ONLY"
    ANY_JSON_VALUE = "ANY_JSON_VALUE"


class DuplicateKeyPolicy(str, Enum):
    REJECT_DUPLICATE_KEYS = "REJECT_DUPLICATE_KEYS"


@dataclass(frozen=True, slots=True)
class JsonInputDescriptor:
    """Immutable provenance and framing contract for one exact byte sequence."""

    source_role: str
    framing_type: JsonFramingType
    encoding: str
    byte_length: int
    content_sha256: str
    container_role: str
    member_role: str
    root_shape: JsonRootShape
    duplicate_key_policy: DuplicateKeyPolicy

    def __post_init__(self) -> None:
        for value in (self.source_role, self.container_role, self.member_role):
            if not isinstance(value, str) or _SAFE_ROLE_RE.fullmatch(value) is None:
                raise ValueError("invalid_governed_role_identifier")
        if not isinstance(self.framing_type, JsonFramingType):
            raise TypeError("invalid_framing_type")
        if not isinstance(self.root_shape, JsonRootShape):
            raise TypeError("invalid_root_shape")
        if not isinstance(self.duplicate_key_policy, DuplicateKeyPolicy):
            raise TypeError("invalid_duplicate_key_policy")
        if not isinstance(self.encoding, str) or not self.encoding.strip():
            raise ValueError("invalid_encoding")
        if not isinstance(self.byte_length, int) or isinstance(self.byte_length, bool) or self.byte_length < 0:
            raise ValueError("invalid_byte_length")
        if not isinstance(self.content_sha256, str) or _SHA256_RE.fullmatch(self.content_sha256) is None:
            raise ValueError("invalid_content_sha256")

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        *,
        source_role: str,
        framing_type: JsonFramingType,
        encoding: str,
        container_role: str,
        member_role: str,
        root_shape: JsonRootShape,
        duplicate_key_policy: DuplicateKeyPolicy = DuplicateKeyPolicy.REJECT_DUPLICATE_KEYS,
    ) -> "JsonInputDescriptor":
        if not isinstance(data, bytes):
            raise TypeError("json_input_must_be_bytes")
        return cls(
            source_role=source_role,
            framing_type=framing_type,
            encoding=encoding,
            byte_length=len(data),
            content_sha256=hashlib.sha256(data).hexdigest(),
            container_role=container_role,
            member_role=member_role,
            root_shape=root_shape,
            duplicate_key_policy=duplicate_key_policy,
        )


class JsonFramingError(ValueError):
    """Stable bounded failure that never retains raw input or filesystem paths."""

    def __init__(
        self,
        reason_code: str,
        *,
        descriptor: JsonInputDescriptor | None = None,
        source_role: str | None = None,
        member_role: str | None = None,
        framing_type: JsonFramingType | None = None,
        line_number: int | None = None,
        offset: int | None = None,
        exception_class: str | None = None,
    ) -> None:
        self.reason_code = reason_code
        self.source_role = descriptor.source_role if descriptor is not None else source_role
        self.member_role = descriptor.member_role if descriptor is not None else member_role
        selected_framing = descriptor.framing_type if descriptor is not None else framing_type
        self.framing_type = selected_framing.value if isinstance(selected_framing, JsonFramingType) else None
        self.byte_length = descriptor.byte_length if descriptor is not None else None
        self.content_sha256 = descriptor.content_sha256 if descriptor is not None else None
        self.line_number = line_number
        self.offset = offset
        self.exception_class = exception_class
        super().__init__(reason_code)

    def as_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in {
                "reason_code": self.reason_code,
                "source_role": self.source_role,
                "member_role": self.member_role,
                "framing_type": self.framing_type,
                "line_number": self.line_number,
                "offset": self.offset,
                "exception_class": self.exception_class,
                "byte_length": self.byte_length,
                "content_sha256": self.content_sha256,
            }.items()
            if value is not None
        }


class _DuplicateKeyError(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError()
        result[key] = value
    return result


def _validate_input(
    data: bytes,
    descriptor: JsonInputDescriptor,
    *,
    framing_type: JsonFramingType,
    expected_source_role: str,
    expected_container_role: str,
    expected_member_role: str,
) -> str:
    if not isinstance(data, bytes):
        raise TypeError("json_input_must_be_bytes")
    if descriptor.source_role != expected_source_role:
        raise JsonFramingError("SOURCE_ROLE_MISMATCH", descriptor=descriptor)
    if descriptor.container_role != expected_container_role:
        raise JsonFramingError("CONTAINER_ROLE_MISMATCH", descriptor=descriptor)
    if descriptor.member_role != expected_member_role:
        raise JsonFramingError("MEMBER_ROLE_MISMATCH", descriptor=descriptor)
    if descriptor.framing_type is not framing_type:
        raise JsonFramingError("FRAMING_TYPE_MISMATCH", descriptor=descriptor)
    if descriptor.duplicate_key_policy is not DuplicateKeyPolicy.REJECT_DUPLICATE_KEYS:
        raise JsonFramingError("DUPLICATE_KEY_POLICY_UNSUPPORTED", descriptor=descriptor)
    if len(data) != descriptor.byte_length:
        raise JsonFramingError("CONTENT_LENGTH_MISMATCH", descriptor=descriptor)
    if hashlib.sha256(data).hexdigest() != descriptor.content_sha256:
        raise JsonFramingError("CONTENT_SHA256_MISMATCH", descriptor=descriptor)
    try:
        return data.decode(descriptor.encoding, errors="strict")
    except LookupError as exc:
        raise JsonFramingError(
            "ENCODING_UNSUPPORTED",
            descriptor=descriptor,
            exception_class=type(exc).__name__,
        ) from exc
    except UnicodeDecodeError as exc:
        raise JsonFramingError(
            "DECODE_FAILED",
            descriptor=descriptor,
            offset=exc.start,
            exception_class=type(exc).__name__,
        ) from exc


def _enforce_root_shape(value: Any, descriptor: JsonInputDescriptor, *, line_number: int | None = None) -> None:
    if descriptor.root_shape is JsonRootShape.OBJECT_ONLY and not isinstance(value, dict):
        raise JsonFramingError("ROOT_SHAPE_OBJECT_REQUIRED", descriptor=descriptor, line_number=line_number)
    if descriptor.root_shape is JsonRootShape.ARRAY_ONLY and not isinstance(value, list):
        raise JsonFramingError("ROOT_SHAPE_ARRAY_REQUIRED", descriptor=descriptor, line_number=line_number)


def parse_single_json_document(
    data: bytes,
    descriptor: JsonInputDescriptor,
    *,
    expected_source_role: str,
    expected_container_role: str,
    expected_member_role: str,
) -> Any:
    """Parse exactly one JSON value with full-consumption and provenance checks."""

    text = _validate_input(
        data,
        descriptor,
        framing_type=JsonFramingType.SINGLE_JSON,
        expected_source_role=expected_source_role,
        expected_container_role=expected_container_role,
        expected_member_role=expected_member_role,
    )
    leading = len(text) - len(text.lstrip())
    decoder = json.JSONDecoder(object_pairs_hook=_reject_duplicate_keys)
    try:
        value, end = decoder.raw_decode(text, idx=leading)
    except _DuplicateKeyError as exc:
        raise JsonFramingError("DUPLICATE_OBJECT_KEY", descriptor=descriptor) from exc
    except json.JSONDecodeError as exc:
        raise JsonFramingError(
            "JSON_DECODE_FAILED",
            descriptor=descriptor,
            line_number=exc.lineno,
            offset=exc.pos,
            exception_class=type(exc).__name__,
        ) from exc
    if text[end:].strip():
        raise JsonFramingError("TRAILING_NONWHITESPACE", descriptor=descriptor, offset=end)
    _enforce_root_shape(value, descriptor)
    return value


def parse_jsonl_records(
    data: bytes,
    descriptor: JsonInputDescriptor,
    *,
    expected_source_role: str,
    expected_container_role: str,
    expected_member_role: str,
    allow_blank_lines: bool,
) -> list[Any]:
    """Parse one JSON value per nonblank line; never parse JSONL as one document."""

    text = _validate_input(
        data,
        descriptor,
        framing_type=JsonFramingType.JSONL,
        expected_source_role=expected_source_role,
        expected_container_role=expected_container_role,
        expected_member_role=expected_member_role,
    )
    rows: list[Any] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            if allow_blank_lines:
                continue
            raise JsonFramingError("BLANK_LINE_NOT_ALLOWED", descriptor=descriptor, line_number=line_number)
        try:
            value = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except _DuplicateKeyError as exc:
            raise JsonFramingError("DUPLICATE_OBJECT_KEY", descriptor=descriptor, line_number=line_number) from exc
        except json.JSONDecodeError as exc:
            raise JsonFramingError(
                "JSONL_RECORD_DECODE_FAILED",
                descriptor=descriptor,
                line_number=line_number,
                offset=exc.pos,
                exception_class=type(exc).__name__,
            ) from exc
        _enforce_root_shape(value, descriptor, line_number=line_number)
        rows.append(value)
    return rows


def serialize_single_json_document(
    value: Any,
    *,
    source_role: str,
    encoding: str,
    container_role: str,
    member_role: str,
    root_shape: JsonRootShape,
    duplicate_key_policy: DuplicateKeyPolicy = DuplicateKeyPolicy.REJECT_DUPLICATE_KEYS,
) -> tuple[bytes, JsonInputDescriptor]:
    """Serialize one value once and bind its exact output bytes to a descriptor."""

    provisional = JsonInputDescriptor(
        source_role=source_role,
        framing_type=JsonFramingType.SINGLE_JSON,
        encoding=encoding,
        byte_length=0,
        content_sha256="0" * 64,
        container_role=container_role,
        member_role=member_role,
        root_shape=root_shape,
        duplicate_key_policy=duplicate_key_policy,
    )
    _enforce_root_shape(value, provisional)
    try:
        data = json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=False,
            allow_nan=False,
        ).encode(encoding, errors="strict")
    except (LookupError, TypeError, UnicodeEncodeError, ValueError) as exc:
        raise JsonFramingError(
            "SERIALIZATION_FAILED",
            descriptor=provisional,
            exception_class=type(exc).__name__,
        ) from exc
    descriptor = JsonInputDescriptor.from_bytes(
        data,
        source_role=source_role,
        framing_type=JsonFramingType.SINGLE_JSON,
        encoding=encoding,
        container_role=container_role,
        member_role=member_role,
        root_shape=root_shape,
        duplicate_key_policy=duplicate_key_policy,
    )
    return data, descriptor
