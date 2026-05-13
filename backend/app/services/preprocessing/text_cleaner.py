import html
import re
import unicodedata


HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
HANDLE_PATTERN = re.compile(r"(?<!\w)@[\w_]+")
HASHTAG_PATTERN = re.compile(r"(?<!\w)#([\w\u4e00-\u9fff]+)")
WHITESPACE_PATTERN = re.compile(r"\s+")
REPEATED_PUNCTUATION_PATTERN = re.compile(r"([!?.,\u3002\uff01\uff1f\uff0c])\1+")
NON_TEXT_PATTERN = re.compile(r"[^\w\s\u4e00-\u9fff!?.,\u3002\uff01\uff1f\uff0c-]")
SPACE_BEFORE_PUNCTUATION_PATTERN = re.compile(r"\s+([!?.,])")
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")
PUNCTUATION_TRANSLATION = str.maketrans(
    {
        "\u3002": ".",
        "\uff01": "!",
        "\uff1f": "?",
        "\uff0c": ",",
    }
)


def normalize_text(text: str) -> str:
    """Normalize Unicode, HTML entities, links, handles, hashtags, punctuation, and spacing."""
    normalized = unicodedata.normalize("NFKC", html.unescape(text or ""))
    normalized = HTML_TAG_PATTERN.sub(" ", normalized)
    normalized = normalized.translate(PUNCTUATION_TRANSLATION)
    normalized = URL_PATTERN.sub(" ", normalized)
    normalized = HANDLE_PATTERN.sub(" ", normalized)
    normalized = HASHTAG_PATTERN.sub(r"\1", normalized)
    normalized = REPEATED_PUNCTUATION_PATTERN.sub(r"\1", normalized)
    normalized = NON_TEXT_PATTERN.sub(" ", normalized)
    normalized = WHITESPACE_PATTERN.sub(" ", normalized)
    normalized = SPACE_BEFORE_PUNCTUATION_PATTERN.sub(r"\1", normalized)
    return normalized.strip()


def clean_text(text: str, *, lowercase: bool = True) -> str:
    cleaned = normalize_text(text)
    if lowercase:
        cleaned = cleaned.lower()
    return cleaned


def detect_language(text: str) -> str:
    if CHINESE_PATTERN.search(text or ""):
        return "zh"
    return "en"


def fingerprint_text(text: str) -> str:
    """Build a stable duplicate-detection fingerprint."""
    cleaned = clean_text(text)
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", cleaned)


class TextCleaner:
    def clean(self, text: str) -> str:
        return clean_text(text)

    def language(self, text: str) -> str:
        return detect_language(text)

    def fingerprint(self, text: str) -> str:
        return fingerprint_text(text)
