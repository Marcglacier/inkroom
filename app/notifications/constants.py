# app/notifications/constants.py

LIKE_POST = "like_post"
COMMENT_POST = "comment_post"
REPOST_POST = "repost_post"

FOLLOW_USER = "follow"
FOLLOW_REQUEST = "follow_request"
FOLLOW_ACCEPT = "follow_accept"

REPLY_COMMENT = "reply_comment"
LIKE_COMMENT = "like_comment"

ALL_NOTIFICATION_TYPES = {
    LIKE_POST,
    COMMENT_POST,
    REPOST_POST,
    FOLLOW_USER,
    FOLLOW_REQUEST,
    FOLLOW_ACCEPT,
    REPLY_COMMENT,
    LIKE_COMMENT,
}