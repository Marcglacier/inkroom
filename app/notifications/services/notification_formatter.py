# app/notifications/services/notification_formatter.py

def format_grouped_notifications(grouped_notifications):
    """
    Converts grouped notifications into API response format
    """

    result = []

    for g in grouped_notifications:

        result.append({
            "type": g["type"],
            "post_id": g["post_id"],
            "comment_id": g["comment_id"],
            "actors": g["actors"],
            "created_at": g["latest_created_at"]
        })

    return result