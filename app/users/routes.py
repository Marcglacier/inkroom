# app/users/routes.py
from flask import Blueprint

from .views.follow_user import FollowUserAPI
from .views.unfollow_user import UnfollowUserAPI

from .views.get_followers import GetFollowersAPI
from .views.get_following import GetFollowingAPI

from .views.get_profile import GetProfileAPI
from .views.update_profile import UpdateProfileAPI

from .views.follow_requests import FollowRequestsAPI
from .views.accept_follow import AcceptFollowAPI
from .views.reject_follow import RejectFollowAPI


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


# =====================
# FOLLOW SYSTEM
# =====================
users_bp.add_url_rule(
    "/<int:user_id>/follow",
    view_func=FollowUserAPI.as_view("follow_user"),
    methods=["POST"]
)

users_bp.add_url_rule(
    "/<int:user_id>/follow",
    view_func=UnfollowUserAPI.as_view("unfollow_user"),
    methods=["DELETE"]
)


# =====================
# FOLLOW REQUESTS
# =====================
users_bp.add_url_rule(
    "/requests",
    view_func=FollowRequestsAPI.as_view("follow_requests"),
    methods=["GET"]
)

users_bp.add_url_rule(
    "/<int:user_id>/follow/accept/<int:follower_id>",
    view_func=AcceptFollowAPI.as_view("accept_follow"),
    methods=["POST"]
)

users_bp.add_url_rule(
    "/<int:user_id>/follow/reject/<int:follower_id>",
    view_func=RejectFollowAPI.as_view("reject_follow"),
    methods=["POST"]
)


# =====================
# SOCIAL GRAPH
# =====================
users_bp.add_url_rule(
    "/<int:user_id>/followers",
    view_func=GetFollowersAPI.as_view("get_followers"),
    methods=["GET"]
)

users_bp.add_url_rule(
    "/<int:user_id>/following",
    view_func=GetFollowingAPI.as_view("get_following"),
    methods=["GET"]
)


# =====================
# PROFILE SYSTEM
# =====================
users_bp.add_url_rule(
    "/<int:user_id>/profile",
    view_func=GetProfileAPI.as_view("get_profile"),
    methods=["GET"]
)

users_bp.add_url_rule(
    "/me/profile",
    view_func=UpdateProfileAPI.as_view("update_profile"),
    methods=["GET", "PATCH"]
)