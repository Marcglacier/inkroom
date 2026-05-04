# app/blog/routes.py
from flask import Blueprint

from .views.create_post import CreatePostAPI
from .views.list_posts import ListPostsAPI
from .views.get_post import GetPostAPI
from .views.update_post import UpdatePostAPI
from .views.delete_post import DeletePostAPI


blog_bp = Blueprint("blog", __name__, url_prefix="/api/posts")

blog_bp.add_url_rule("", view_func=CreatePostAPI.as_view("create_post"), methods=["POST"])
blog_bp.add_url_rule("", view_func=ListPostsAPI.as_view("list_posts"), methods=["GET"])
blog_bp.add_url_rule("/<int:post_id>", view_func=GetPostAPI.as_view("get_post"), methods=["GET"])
blog_bp.add_url_rule("/<int:post_id>", view_func=UpdatePostAPI.as_view("update_post"), methods=["PUT"])
blog_bp.add_url_rule("/<int:post_id>", view_func=DeletePostAPI.as_view("delete_post"), methods=["DELETE"])