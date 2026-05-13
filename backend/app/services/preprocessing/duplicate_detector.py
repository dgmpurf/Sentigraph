from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
import hashlib

from app.schemas.comment import CleanComment, RawComment
from app.services.preprocessing.text_cleaner import clean_text, detect_language, fingerprint_text


@dataclass(frozen=True)
class DuplicateDetectionConfig:
    similarity_threshold: float = 0.92
    repeated_script_threshold: int = 3


def _similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def _fingerprint_hash(fingerprint: str) -> str:
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


def _find_group_index(
    fingerprint: str,
    group_fingerprints: list[str],
    group_hashes: list[str],
    threshold: float,
) -> int | None:
    fingerprint_hash = _fingerprint_hash(fingerprint)
    for index, existing_hash in enumerate(group_hashes):
        if fingerprint_hash == existing_hash:
            return index
    for index, existing in enumerate(group_fingerprints):
        if _similarity(fingerprint, existing) >= threshold:
            return index
    return None


def detect_duplicate_groups(
    comments: list[RawComment],
    config: DuplicateDetectionConfig | None = None,
) -> list[CleanComment]:
    config = config or DuplicateDetectionConfig()
    groups: list[list[RawComment]] = []
    group_fingerprints: list[str] = []
    group_hashes: list[str] = []

    for comment in comments:
        fingerprint = fingerprint_text(comment.content)
        group_index = _find_group_index(
            fingerprint,
            group_fingerprints,
            group_hashes,
            config.similarity_threshold,
        )
        if group_index is None:
            groups.append([comment])
            group_fingerprints.append(fingerprint)
            group_hashes.append(_fingerprint_hash(fingerprint))
        else:
            groups[group_index].append(comment)

    clean_comments: list[CleanComment] = []
    clean_index = 1
    for group_index, group in enumerate(groups, start=1):
        global_duplicate_count = len(group)
        duplicate_group_id = f"dup_group_{group_index:03d}" if global_duplicate_count > 1 else None
        semantic_group = f"sem_group_{group_index:03d}"
        is_repeated_script = global_duplicate_count >= config.repeated_script_threshold
        comments_by_author: dict[str, list[RawComment]] = defaultdict(list)
        for comment in group:
            comments_by_author[str(comment.author_id)].append(comment)

        for author_id, author_group in sorted(comments_by_author.items()):
            first = author_group[0]
            clean_text_value = clean_text(first.content)
            created_values = sorted(comment.created_at for comment in author_group)
            clean_comments.append(
                CleanComment(
                    clean_comment_id=f"clean_{clean_index:03d}",
                    original_comment_ids=[comment.comment_id for comment in author_group],
                    platforms=sorted({comment.platform for comment in author_group}),
                    post_ids=sorted({comment.post_id for comment in author_group}),
                    author_id=author_id,
                    clean_text=clean_text_value,
                    language=detect_language(clean_text_value),
                    duplicate_group_id=duplicate_group_id,
                    duplicate_count=len(author_group),
                    semantic_similarity_group=semantic_group,
                    is_repeated_script=is_repeated_script,
                    created_at_min=created_values[0],
                    created_at_max=created_values[-1],
                )
            )
            clean_index += 1
    return clean_comments


def group_duplicate_counts(clean_comments: list[CleanComment]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for comment in clean_comments:
        key = comment.duplicate_group_id or comment.clean_comment_id
        counts[str(key)] += comment.duplicate_count
    return dict(counts)
