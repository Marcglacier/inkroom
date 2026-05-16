# app/feed/routes.py
from flask import Blueprint
from .views.following_feed import FollowingFeedAPI
from .views.for_you_feed import ForYouFeedAPI


feed_bp = Blueprint("feed", __name__, url_prefix="/api/feed")

feed_bp.add_url_rule(
    "/following",
    view_func=FollowingFeedAPI.as_view("following_feed"),
    methods=["GET"]
)

feed_bp.add_url_rule(
    "/for-you",
    view_func=ForYouFeedAPI.as_view("for_you_feed"),
    methods=["GET"]
)