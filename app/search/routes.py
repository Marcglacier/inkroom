# app/search/routes.py
from flask import Blueprint
from .views.search import SearchAPI

search_bp = Blueprint("search", __name__, url_prefix="/api/search")
search_bp.add_url_rule("", view_func=SearchAPI.as_view("search"), methods=["GET"])