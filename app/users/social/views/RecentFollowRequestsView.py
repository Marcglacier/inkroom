from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.social.services.get_recent_follow_requests import (
    get_recent_follow_requests
)


class RecentFollowRequestsView(MethodView):

    decorators = [jwt_required()]

    def get(self):
        print("RECENT FOLLOW REQUESTS QUERY HIT")

        user_id = int(get_jwt_identity())
        results = get_recent_follow_requests(user_id)

        print("RESULT:", results)

        return {"requests": results}, 200