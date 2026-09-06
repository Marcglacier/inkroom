# app/users/profile/services/social_links/social_link_service.py
from app.users.profile.services.social_links.social_link_detector import (
    SocialLinkDetector,
)

from app.users.profile.services.social_links.social_link_normalizer import (
    SocialLinkNormalizer,
)


class SocialLinkService:
    """
    Processes profile social links.

    Responsibilities:
    - Accept raw URLs
    - Normalize URLs
    - Detect platform
    - Reject unsupported platforms
    - Prevent duplicates
    - Return frontend-ready structures
    """

    def __init__(self, social_links):
        self.social_links = social_links or []

    def execute(self) -> list[dict]:
        processed = []

        for item in self.social_links:
            url = self._extract_url(item)

            if not url:
                continue

            link = self._process_url(url)

            if not self._is_duplicate(
                processed,
                link["url"],
            ):
                processed.append(link)

        return processed

    # =========================
    # INPUT
    # =========================

    def _extract_url(self, item) -> str | None:
        if isinstance(item, str):
            return item.strip()

        if isinstance(item, dict):
            url = item.get("url")

            if isinstance(url, str):
                return url.strip()

        return None

    # =========================
    # PROCESSING
    # =========================

    def _process_url(self, url: str) -> dict:
        normalized_url = SocialLinkNormalizer(
            url
        ).normalize()

        platform = SocialLinkDetector(
            normalized_url
        ).detect()

        if not platform:
            raise ValueError(
                f"Unsupported social platform: {url}"
            )

        return {
            "platform": platform,
            "url": normalized_url,
        }

    # =========================
    # DUPLICATES
    # =========================

    @staticmethod
    def _is_duplicate(
        processed: list[dict],
        url: str,
    ) -> bool:
        return any(
            link["url"] == url
            for link in processed
        )