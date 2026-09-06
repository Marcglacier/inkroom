# app/inbox/api/search/search_inbox_api.py

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.search.search_inbox import SearchInboxService



class SearchInboxAPI(MethodView):


    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        text = request.args.get("q","").strip()



        if not text:

            return jsonify({

                "results":[]

            }),200

        results = ( SearchInboxService( user_id=user_id, text=text, ).execute())
        return jsonify({ "results": results}), 200