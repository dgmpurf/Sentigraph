from __future__ import annotations

import uuid
from datetime import datetime, timezone


def utc_compact_timestamp() -> str:
    """Return the existing Analysis Requests compact UTC timestamp format."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def generate_record_id(prefix: str) -> str:
    """Return an Analysis Requests record id with the existing prefix/timestamp/suffix shape."""
    normalized_prefix = prefix.strip()
    if not normalized_prefix:
        raise ValueError("record id prefix is required")
    return f"{normalized_prefix}_{utc_compact_timestamp()}_{uuid.uuid4().hex[:8]}"

