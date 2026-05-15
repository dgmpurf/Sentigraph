from __future__ import annotations

import os
from typing import Any

from app.services.storage.base_store import CaseStore
from app.services.storage.local_json_store import LocalJsonCaseStore
from app.services.storage.mongodb_store import MongoClientFactory, MongoDbCaseStore


LOCAL_JSON_BACKENDS = {"", "local_json", "json"}
MONGODB_BACKENDS = {"mongodb", "mongo"}


def create_case_store_from_env(
    *,
    mongo_client_factory: MongoClientFactory | None = None,
    mongo_verify_connection: bool = True,
) -> CaseStore:
    """Create the configured case store.

    Defaults to local JSON so normal development and tests do not require
    MongoDB. MongoDB is opt-in through `CASE_STORE_BACKEND=mongodb`.
    """

    backend = os.getenv("CASE_STORE_BACKEND", "local_json").strip().lower()
    if backend in LOCAL_JSON_BACKENDS:
        return LocalJsonCaseStore(os.getenv("CASE_STORE_PATH") or None)
    if backend in MONGODB_BACKENDS:
        return MongoDbCaseStore.from_env(
            client_factory=mongo_client_factory,
            verify_connection=mongo_verify_connection,
        )
    allowed = ", ".join(sorted(LOCAL_JSON_BACKENDS | MONGODB_BACKENDS))
    raise ValueError(f"Unsupported CASE_STORE_BACKEND='{backend}'. Expected one of: {allowed}.")
