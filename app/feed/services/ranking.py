# app/feed/services/ranking.py
from datetime import datetime

def compute_post_score(post):
    """
    Simple engagement ranking model (v1)
    """

    likes = post.likes_count or 0
    comments = post.comments_count or 0
    reposts = post.reposts_count or 0

    # recency boost (newer posts rank higher)
    hours_old = (datetime.utcnow() - post.created_at).total_seconds() / 3600
    recency_boost = max(0, 24 - hours_old) * 0.5

    score = (
        likes * 1 +
        comments * 2 +
        reposts * 3 +
        recency_boost
    )

    return score