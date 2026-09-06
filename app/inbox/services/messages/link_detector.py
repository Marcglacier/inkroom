# app/inbox/services/messages/link_detector.py
import re
from urllib.parse import urlparse, urlunparse


URL_PATTERN = re.compile(
    r"""
    (?<![\w@])
    (?:
        https?://
        |
        www\.
    )
    [^\s<>"']+
    """,
    re.IGNORECASE | re.VERBOSE,
)


TRAILING_PUNCTUATION = ".,!?;:)]}>\"'"


def detect_links(text: str | None) -> list[str]:
    """
    Extract URLs from message text.

    Supports:
        https://example.com
        http://example.com
        www.example.com
    """

    if not text:
        return []

    matches = URL_PATTERN.findall(text)

    links = []

    for url in matches:
        url = url.rstrip(TRAILING_PUNCTUATION)

        if not url:
            continue

        if url not in links:
            links.append(url)

    return links


def normalize_url(url: str) -> str:
    """
    Normalize a URL so equivalent URLs can be compared/stored consistently.
    """

    url = url.strip()

    if not url:
        return url

    if url.lower().startswith("www."):
        url = f"https://{url}"

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Remove default ports
    if netloc.endswith(":80") and scheme == "http":
        netloc = netloc[:-3]

    if netloc.endswith(":443") and scheme == "https":
        netloc = netloc[:-4]

    # Remove trailing slash from path except root
    path = parsed.path

    if path == "/":
        path = ""

    elif path.endswith("/"):
        path = path.rstrip("/")

    normalized = urlunparse(
        (
            scheme,
            netloc,
            path,
            "",
            parsed.query,
            "",
        )
    )

    return normalized