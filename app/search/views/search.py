# app/search/views/search.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.jwt_debug import debug_jwt
from app.search.services.search_service import global_search


class SearchAPI(MethodView):

    @jwt_required()
    def get(self):

        print("===== SEARCH REQUEST =====")
        print("QUERY:", request.args.get("q"))

        debug_jwt("SEARCH ROUTE")

        query = request.args.get("q", "")

        result = global_search(query)

        return jsonify(result), 200