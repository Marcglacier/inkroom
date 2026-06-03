from datetime import datetime


def format_joined_at(user):
    if not user.created_at:
        return None
    return user.created_at.strftime("%B %Y")


def safe_iso(date_value):
    return date_value.isoformat() if date_value else None