import logging
from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.models.user import User

log = logging.getLogger(__name__)


class FollowService:

    # -------------------------
    # helpers
    # -------------------------
    @staticmethod
    def _res(msg, status, **extra):
        return {"message": msg, "status": status, **extra}

    # -------------------------
    # follow
    # -------------------------
    @staticmethod
    def follow_user(u, t):

        if u == t:
            return {"error": "Cannot follow yourself"}, 400

        user = User.query.get(t)
        if not user:
            return {"error": "User not found"}, 404

        f = Follow.query.filter_by(follower_id=u, following_id=t).first()
        if f:
            return FollowService._res("Already following", "following",
                                      follower_id=u, following_id=t)

        if user.is_private:
            r = FollowRequest.query.filter_by(requester_id=u, target_id=t).first()
            if r:
                return FollowService._res("Request already sent", "requested",
                                          follower_id=u, following_id=t)

            db.session.add(FollowRequest(requester_id=u, target_id=t))
            db.session.commit()

            return FollowService._res("Follow request sent", "requested",
                                      follower_id=u, following_id=t)

        db.session.add(Follow(follower_id=u, following_id=t))
        db.session.commit()

        return FollowService._res("User followed", "following",
                                  follower_id=u, following_id=t)

    # -------------------------
    # unfollow
    # -------------------------
    @staticmethod
    def unfollow_user(u, t):

        f = Follow.query.filter_by(follower_id=u, following_id=t).first()
        if not f:
            return {"error": "Not following"}, 400

        db.session.delete(f)
        db.session.commit()

        return FollowService._res("User unfollowed", "unfollowed",
                                  follower_id=u, following_id=t)

    # -------------------------
    # accept
    # -------------------------
    @staticmethod
    def accept_follow(u, r):

        req = FollowRequest.query.filter_by(
            requester_id=r, target_id=u
        ).first()

        if not req:
            return {"error": "Request not found"}, 404

        db.session.add(Follow(follower_id=r, following_id=u))
        db.session.delete(req)
        db.session.commit()

        return FollowService._res("Follow request accepted", "following",
                                  follower_id=r, following_id=u)

    # -------------------------
    # reject
    # -------------------------
    @staticmethod
    def reject_follow(u, r):

        req = FollowRequest.query.filter_by(
            requester_id=r, target_id=u
        ).first()

        if not req:
            return {"error": "Request not found"}, 404

        db.session.delete(req)
        db.session.commit()

        return FollowService._res("Follow request rejected", "rejected",
                                  follower_id=r, following_id=u)