from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.users.services.relationship_service import get_relationship


class RelationshipAPI(MethodView):

    @jwt_required()
    def get(self, user_id):

        current_user_id = int(get_jwt_identity())

        result = get_relationship(
            current_user_id,
            user_id
        )

        return jsonify(result), 200