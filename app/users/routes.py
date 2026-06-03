# app/users/routes.py

from flask import Blueprint
from .social.views.follow_user import FollowUserAPI
from .social.views.get_followers import GetFollowersAPI
from .profile.views.get_profile import GetProfileAPI
from .profile.views.update_profile import UpdateProfileAPI
from .social.views.follow_requests import FollowRequestsAPI
from .social.views.accept_follow import AcceptFollowAPI
from .social.views.reject_follow import RejectFollowAPI
from .social.views.upload_avatar import UploadAvatarAPI
from .social.views.unfollow_user import UnfollowUserAPI
from .social.views.get_following import GetFollowingAPI
from .profile.views.get_user_by_username import GetUserByUsernameAPI
from .social.views.relationship_view import RelationshipAPI

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

# =====================
# FOLLOW SYSTEM
# =====================
users_bp.add_url_rule("/<int:user_id>/follow",
    view_func=FollowUserAPI.as_view("follow_user"), methods=["POST"])
users_bp.add_url_rule("/<int:user_id>/follow",
    view_func=UnfollowUserAPI.as_view("unfollow_user"), methods=["DELETE"])

# =====================
# FOLLOW REQUESTS
# =====================
users_bp.add_url_rule("/requests",
    view_func=FollowRequestsAPI.as_view("follow_requests"), methods=["GET"])
users_bp.add_url_rule("/<int:user_id>/follow/accept/<int:follower_id>",
    view_func=AcceptFollowAPI.as_view("accept_follow"), methods=["POST"])
users_bp.add_url_rule("/<int:user_id>/follow/reject/<int:follower_id>",
    view_func=RejectFollowAPI.as_view("reject_follow"), methods=["POST"])

# =====================
# SOCIAL GRAPH
# =====================
users_bp.add_url_rule("/<int:user_id>/followers",
    view_func=GetFollowersAPI.as_view("get_followers"), methods=["GET"])
users_bp.add_url_rule("/<int:user_id>/following",
    view_func=GetFollowingAPI.as_view("get_following"), methods=["GET"])

# =====================
# PROFILE SYSTEM
# =====================
users_bp.add_url_rule("/<int:user_id>/profile",
    view_func=GetProfileAPI.as_view("get_profile"), methods=["GET"])
users_bp.add_url_rule("/me/profile",
    view_func=UpdateProfileAPI.as_view("update_profile"), methods=["GET", "PATCH"])

# =====================
# AVATAR UPLOAD
# =====================
users_bp.add_url_rule("/upload",
    view_func=UploadAvatarAPI.as_view("upload_avatar"), methods=["POST"])

# =====================
# USER INFO
# =====================
users_bp.add_url_rule(
    "/<string:username>",
    view_func=GetUserByUsernameAPI.as_view("get_user_by_username")
)

users_bp.add_url_rule(
    "/<int:user_id>/relationship",
    view_func=RelationshipAPI.as_view("relationship")
)
