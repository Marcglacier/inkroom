import re

def clean_username(raw: str) -> str:
    """
    Rules:
    - lowercase only
    - allowed: a-z, 0-9, underscore (_), dot (.)
    - no spaces
    - min length: 6
    - cannot start or end with '.' or '_'
    """

    username = (raw or "user").lower().strip()

    # replace invalid chars with underscore
    username = re.sub(r"[^a-z0-9._]", "_", username)

    # collapse multiple special chars
    username = re.sub(r"[._]+", lambda m: m.group(0)[0], username)

    # remove leading/trailing . or _
    username = username.strip("._")

    # enforce minimum length
    if len(username) < 6:
        username = f"{username}_user"

    # final safety trim again
    username = username.strip("._")

    return username