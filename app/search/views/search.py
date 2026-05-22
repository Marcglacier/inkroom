# app/search/views/search.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.search.services.search_service import global_search


class SearchAPI(MethodView):

    @jwt_required()
    def get(self):

        query = request.args.get("q", "")

        result = global_search(query)

        return jsonify(result), 200