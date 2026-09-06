# app/users/profile/services/social_links/social_link_detector.py
from urllib.parse import urlparse


class SocialLinkDetector:
    """
    Detects supported social-media platforms from URLs.

    This service is responsible only for platform detection.
    It does not mutate the database.
    """

    PLATFORM_DOMAINS = {
        "instagram": {
            "instagram.com",
        },

        "youtube": {
            "youtube.com",
            "youtu.be",
        },

        "tiktok": {
            "tiktok.com",
        },

        "facebook": {
            "facebook.com",
            "fb.com",
        },

        "x": {
            "x.com",
            "twitter.com",
        },

        "linkedin": {
            "linkedin.com",
        },

        "threads": {
            "threads.net",
        },

        "snapchat": {
            "snapchat.com",
        },

        "pinterest": {
            "pinterest.com",
        },

        "reddit": {
            "reddit.com",
        },

        "telegram": {
            "t.me",
            "telegram.me",
            "telegram.org",
        },

        "whatsapp": {
            "whatsapp.com",
            "wa.me",
        },

        "github": {
            "github.com",
        },

        "twitch": {
            "twitch.tv",
        },
    }

    def __init__(self, url: str):
        self.url = url

    def detect(self) -> str | None:
        hostname = self._get_hostname()

        if not hostname:
            return None

        return self._find_platform(hostname)

    def _get_hostname(self) -> str | None:
        try:
            parsed = urlparse(self.url)

            hostname = parsed.hostname

            if not hostname:
                return None

            return hostname.lower().strip(".")

        except (ValueError, AttributeError):
            return None

    def _find_platform(self, hostname: str) -> str | None:
        for platform, domains in self.PLATFORM_DOMAINS.items():
            for domain in domains:
                if self._matches_domain(
                    hostname,
                    domain,
                ):
                    return platform

        return None

    @staticmethod
    def _matches_domain(
        hostname: str,
        domain: str,
    ) -> bool:
        return (
            hostname == domain
            or hostname.endswith(f".{domain}")
        )