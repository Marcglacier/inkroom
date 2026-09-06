# app/users/profile/services/social_links/social_link_normalizer.py
from urllib.parse import urlparse, urlunparse


class SocialLinkNormalizer:
    """
    Normalizes social URLs before they are stored.
    """

    def __init__(self, url: str):
        self.url = url

    def normalize(self) -> str:
        url = self.url.strip()

        parsed = urlparse(url)

        if parsed.scheme.lower() not in {
            "http",
            "https",
        }:
            raise ValueError(
                "Social link must use HTTP or HTTPS."
            )

        if not parsed.netloc:
            raise ValueError(
                "Invalid social link URL."
            )

        return urlunparse(
            (
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path,
                "",
                parsed.query,
                "",
            )
        )