from __future__ import annotations

import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from app.core.environment import load_project_env
from app.services.crawling.public_parser.robots_checker import RobotsChecker
from app.services.crawling.public_parser.selector_profile import SelectorProfile


DEFAULT_PUBLIC_PARSER_USER_AGENT = "sentigraph-public-parser-dev"


@dataclass(frozen=True)
class PublicFetchResult:
    ok: bool
    url: str
    html: str | None = None
    status_code: int | None = None
    fallback_reason_category: str | None = None
    message: str = ""
    live_fetch_enabled: bool = False
    request_headers: dict[str, str] = field(default_factory=dict)


class PublicFetcher:
    """Conservative fetcher for public pages.

    Live fetching is disabled by default. The fetcher never sends cookies,
    authorization headers, browser-profile state, or proxy settings.
    """

    def __init__(
        self,
        *,
        live_fetch_enabled: bool = False,
        rate_limit_seconds: float = 3.0,
        user_agent: str = DEFAULT_PUBLIC_PARSER_USER_AGENT,
        timeout_seconds: float = 5.0,
        max_retries: int = 0,
    ) -> None:
        self.live_fetch_enabled = live_fetch_enabled
        self.rate_limit_seconds = max(float(rate_limit_seconds), 0.0)
        self.user_agent = user_agent.strip() or DEFAULT_PUBLIC_PARSER_USER_AGENT
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(0, min(int(max_retries), 1))
        self._last_fetch_at = 0.0

    @classmethod
    def from_env(cls, *, default_rate_limit_seconds: float = 3.0) -> "PublicFetcher":
        load_project_env()
        live_fetch_enabled = os.getenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false").strip().lower() == "true"
        rate_limit_text = os.getenv("PUBLIC_PARSER_RATE_LIMIT_SECONDS", str(default_rate_limit_seconds))
        try:
            rate_limit_seconds = float(rate_limit_text)
        except ValueError:
            rate_limit_seconds = default_rate_limit_seconds
        user_agent = os.getenv("PUBLIC_PARSER_USER_AGENT", DEFAULT_PUBLIC_PARSER_USER_AGENT)
        return cls(
            live_fetch_enabled=live_fetch_enabled,
            rate_limit_seconds=rate_limit_seconds,
            user_agent=user_agent,
        )

    def build_request(self, url: str) -> urllib.request.Request:
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml",
        }
        return urllib.request.Request(url, headers=headers, method="GET")

    def fetch(self, url: str, profile: SelectorProfile) -> PublicFetchResult:
        request = self.build_request(url)
        request_headers = {key: str(value) for key, value in request.header_items()}

        if not self.live_fetch_enabled:
            return PublicFetchResult(
                ok=False,
                url=url,
                fallback_reason_category="live_fetch_disabled",
                message="Live public-page fetching is disabled by configuration.",
                live_fetch_enabled=False,
                request_headers=request_headers,
            )

        robots = RobotsChecker(live_fetch_enabled=True, user_agent=self.user_agent).can_fetch(url, profile)
        if not robots.allowed:
            return PublicFetchResult(
                ok=False,
                url=url,
                fallback_reason_category=robots.reason,
                message="Robots/profile policy did not allow fetching.",
                live_fetch_enabled=True,
                request_headers=request_headers,
            )

        self._respect_rate_limit()
        attempts = self.max_retries + 1
        for attempt in range(attempts):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    status_code = getattr(response, "status", None)
                    content_type = response.headers.get("Content-Type", "")
                    html = response.read(1_000_000).decode(_encoding_from_content_type(content_type), errors="replace")
                    return PublicFetchResult(
                        ok=True,
                        url=url,
                        html=html,
                        status_code=status_code,
                        live_fetch_enabled=True,
                        request_headers=request_headers,
                    )
            except urllib.error.HTTPError as exc:
                return PublicFetchResult(
                    ok=False,
                    url=url,
                    status_code=exc.code,
                    fallback_reason_category="http_error",
                    message="Public page returned an HTTP error.",
                    live_fetch_enabled=True,
                    request_headers=request_headers,
                )
            except (TimeoutError, urllib.error.URLError):
                if attempt >= attempts - 1:
                    return PublicFetchResult(
                        ok=False,
                        url=url,
                        fallback_reason_category="network_error",
                        message="Public page fetch failed with a network error.",
                        live_fetch_enabled=True,
                        request_headers=request_headers,
                    )

        return PublicFetchResult(
            ok=False,
            url=url,
            fallback_reason_category="network_error",
            message="Public page fetch failed.",
            live_fetch_enabled=True,
            request_headers=request_headers,
        )

    def _respect_rate_limit(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_fetch_at
        if elapsed < self.rate_limit_seconds:
            time.sleep(self.rate_limit_seconds - elapsed)
        self._last_fetch_at = time.monotonic()


def _encoding_from_content_type(content_type: str) -> str:
    for part in content_type.split(";"):
        part = part.strip().lower()
        if part.startswith("charset="):
            return part.split("=", 1)[1] or "utf-8"
    return "utf-8"

