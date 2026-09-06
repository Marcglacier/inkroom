# app/inbox/services/messages/link_preview.py

import ipaddress
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


REQUEST_TIMEOUT = 5

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; InkRoomLinkPreview/1.0)"
)


PLATFORM_DOMAINS = {
    "youtube.com": "youtube",
    "youtu.be": "youtube",

    "instagram.com": "instagram",

    "tiktok.com": "tiktok",

    "facebook.com": "facebook",
    "fb.com": "facebook",

    "x.com": "x",
    "twitter.com": "x",

    "linkedin.com": "linkedin",

    "github.com": "github",
}


def _is_private_host(hostname: str) -> bool:
    """
    Prevent SSRF requests to localhost/private networks.
    """

    if not hostname:
        return True

    hostname = hostname.lower().strip(".")

    if hostname in {
        "localhost",
        "localhost.localdomain",
    }:
        return True

    try:
        addresses = socket.getaddrinfo(
            hostname,
            None,
        )

        for address in addresses:
            ip = ipaddress.ip_address(
                address[4][0]
            )

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
            ):
                return True

    except (socket.gaierror, ValueError):
        return True

    return False


def _get_platform(domain: str) -> str:
    domain = domain.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    for known_domain, platform in PLATFORM_DOMAINS.items():
        if (
            domain == known_domain
            or domain.endswith("." + known_domain)
        ):
            return platform

    return "generic"


def _meta_content(
    soup: BeautifulSoup,
    *,
    property_name: str | None = None,
    name: str | None = None,
):
    if property_name:
        tag = soup.find(
            "meta",
            attrs={"property": property_name},
        )
    else:
        tag = soup.find(
            "meta",
            attrs={"name": name},
        )

    if not tag:
        return None

    return tag.get("content")


def fetch_link_preview(url: str) -> dict:
    """
    Fetch Open Graph / HTML metadata for a URL.

    Returns safe preview data even when metadata is missing.
    """

    parsed = urlparse(url)

    if parsed.scheme.lower() not in {
        "http",
        "https",
    }:
        raise ValueError("Only HTTP/HTTPS URLs are supported.")

    hostname = parsed.hostname

    if _is_private_host(hostname):
        raise ValueError(
            "Private or local URLs are not allowed."
        )

    response = requests.get(
        url,
        headers={
            "User-Agent": USER_AGENT,
        },
        timeout=REQUEST_TIMEOUT,
        allow_redirects=True,
        stream=True,
    )

    response.raise_for_status()

    final_url = response.url

    final_parsed = urlparse(final_url)

    if final_parsed.scheme.lower() not in {
        "http",
        "https",
    }:
        raise ValueError(
            "Redirected to an unsupported URL scheme."
        )

    if _is_private_host(final_parsed.hostname):
        raise ValueError(
            "Redirected to a private or local URL."
        )

    content_type = (
        response.headers
        .get("Content-Type", "")
        .lower()
    )

    if "text/html" not in content_type:
        return {
            "title": None,
            "description": None,
            "image_url": None,
            "site_name": final_parsed.hostname,
            "domain": final_parsed.hostname,
            "platform": _get_platform(
                final_parsed.hostname or ""
            ),
            "content_type": "generic",
        }

    # Don't allow giant responses.
    max_bytes = 2 * 1024 * 1024

    chunks = []
    total = 0

    for chunk in response.iter_content(
        chunk_size=8192
    ):
        if not chunk:
            continue

        total += len(chunk)

        if total > max_bytes:
            break

        chunks.append(chunk)

    html = b"".join(chunks)

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = (
        _meta_content(
            soup,
            property_name="og:title",
        )
        or (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else None
        )
    )

    description = (
        _meta_content(
            soup,
            property_name="og:description",
        )
        or _meta_content(
            soup,
            name="description",
        )
    )

    image_url = _meta_content(
        soup,
        property_name="og:image",
    )

    site_name = _meta_content(
        soup,
        property_name="og:site_name",
    )

    domain = final_parsed.hostname

    platform = _get_platform(
        domain or ""
    )

    og_type = _meta_content(
        soup,
        property_name="og:type",
    )

    if platform != "generic":
        preview_type = "social"
    elif og_type:
        preview_type = og_type
    else:
        preview_type = "article"

    return {
        "title": title.strip() if title else None,
        "description": (
            description.strip()
            if description
            else None
        ),
        "image_url": image_url,
        "site_name": site_name,
        "domain": domain,
        "platform": platform,
        "content_type": preview_type,
    }