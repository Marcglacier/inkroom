# app/users/routes.py
from flask import Blueprint

from .views.follow_user import FollowUserAPI
from .views.unfollow_user import UnfollowUserAPI
from .views.get_followers import GetFollowersAPI
from .views.get_following import GetFollowingAPI
from .views.get_profile import GetProfileAPI
from .views.update_profile import UpdateProfileAPI

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users"
)

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

users_bp.add_url_rule(
    "/<int:user_id>/profile",
    view_func=GetProfileAPI.as_view("get_profile"),
    methods=["GET"]
)

users_bp.add_url_rule(
    "/me/profile",
    view_func=UpdateProfileAPI.as_view("update_profile"),
    methods=["PATCH"]
)