from __future__ import annotations


class PublicParserError(RuntimeError):
    """Base class for public parser failures."""


class PublicParserDisabledError(PublicParserError):
    """Raised when live public parsing is disabled by configuration."""


class SelectorProfileError(PublicParserError):
    """Raised when a selector profile is missing or invalid."""


class PublicFetchError(PublicParserError):
    """Raised when a public fetch cannot be completed safely."""


class RobotsDisallowedError(PublicFetchError):
    """Raised when robots.txt or profile path policy does not allow fetching."""

