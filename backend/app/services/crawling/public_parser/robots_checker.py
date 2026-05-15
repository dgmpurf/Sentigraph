from __future__ import annotations

import urllib.parse
import urllib.robotparser
import urllib.request
from dataclasses import dataclass

from app.services.crawling.public_parser.selector_profile import SelectorProfile


@dataclass(frozen=True)
class RobotsCheckResult:
    allowed: bool
    reason: str
    robots_url: str


class RobotsChecker:
    """Small robots/policy helper for public-page parsing.

    If robots access is unclear, the checker returns not allowed. This keeps
    live parsing opt-in and conservative.
    """

    def __init__(self, *, live_fetch_enabled: bool, user_agent: str, timeout_seconds: float = 5.0) -> None:
        self.live_fetch_enabled = live_fetch_enabled
        self.user_agent = user_agent
        self.timeout_seconds = timeout_seconds

    def can_fetch(self, url: str, profile: SelectorProfile) -> RobotsCheckResult:
        robots_url = self._robots_url(url)
        if not self.live_fetch_enabled:
            return RobotsCheckResult(False, "live_fetch_disabled", robots_url)
        if not _path_allowed_by_profile(url, profile.allowed_public_paths):
            return RobotsCheckResult(False, "path_not_allowed_by_profile", robots_url)
        parser = urllib.robotparser.RobotFileParser(robots_url)
        try:
            request = urllib.request.Request(
                robots_url,
                headers={
                    "User-Agent": self.user_agent,
                    "Accept": "text/plain",
                },
                method="GET",
            )
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                lines = response.read(200_000).decode("utf-8", errors="replace").splitlines()
            parser.parse(lines)
        except Exception:
            return RobotsCheckResult(False, "robots_unavailable_or_unclear", robots_url)
        return RobotsCheckResult(parser.can_fetch(self.user_agent, url), "robots_allowed" if parser.can_fetch(self.user_agent, url) else "robots_disallowed", robots_url)

    @staticmethod
    def _robots_url(url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))


def _path_allowed_by_profile(url: str, allowed_public_paths: list[str]) -> bool:
    if not allowed_public_paths:
        return False
    path = urllib.parse.urlparse(url).path or "/"
    return any(path.startswith(allowed_path) for allowed_path in allowed_public_paths)
