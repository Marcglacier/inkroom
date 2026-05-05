import logging
from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.models.user import User

log = logging.getLogger(__name__)


class FollowService:

    # =========================
    # FOLLOW
    # =========================
    @staticmethod
    def follow_user(current_user_id, target_user_id):

        if current_user_id == target_user_id:
            return {"error": "Cannot follow yourself"}, 400

        user = User.query.get(target_user_id)
        if not user:
            return {"error": "User not found"}, 404

        # already following check
        existing_follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=target_user_id
        ).first()

        if existing_follow:
            return {
                "message": "Already following",
                "status": "following",
                "follower_id": current_user_id,
                "following_id": target_user_id
            }

        # =========================
        # PRIVATE → REQUEST FLOW
        # =========================
        if user.is_private:

            existing_req = FollowRequest.query.filter_by(
                requester_id=current_user_id,
                target_id=target_user_id
            ).first()

            if existing_req:
                return {
                    "message": "Request already sent",
                    "status": "requested",
                    "follower_id": current_user_id,
                    "following_id": target_user_id
                }

            db.session.add(FollowRequest(
                requester_id=current_user_id,
                target_id=target_user_id
            ))
            db.session.commit()

            return {
                "message": "Follow request sent",
                "status": "requested",
                "follower_id": current_user_id,
                "following_id": target_user_id
            }

        # =========================
        # PUBLIC → DIRECT FOLLOW
        # =========================
        db.session.add(Follow(
            follower_id=current_user_id,
            following_id=target_user_id
        ))
        db.session.commit()

        return {
            "message": "User followed",
            "status": "following",
            "follower_id": current_user_id,
            "following_id": target_user_id
        }

    # =========================
    # UNFOLLOW
    # =========================
    @staticmethod
    def unfollow_user(current_user_id, target_user_id):

        follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=target_user_id
        ).first()

        if not follow:
            return {"error": "Not following"}, 400

        db.session.delete(follow)
        db.session.commit()

        return {
            "message": "User unfollowed",
            "status": "unfollowed",
            "follower_id": current_user_id,
            "following_id": target_user_id
        }

    # =========================
    # ACCEPT FOLLOW REQUEST
    # =========================
    @staticmethod
    def accept_follow(target_user_id, requester_id):

        req = FollowRequest.query.filter_by(
            requester_id=requester_id,
            target_id=target_user_id
        ).first()

        if not req:
            return {"error": "Request not found"}, 404

        follow = Follow.query.filter_by(
            follower_id=requester_id,
            following_id=target_user_id
        ).first()

        if not follow:
            db.session.add(Follow(
                follower_id=requester_id,
                following_id=target_user_id
            ))

        db.session.delete(req)
        db.session.commit()

        return {
            "message": "Follow request accepted",
            "status": "following",
            "follower_id": requester_id,
            "following_id": target_user_id
        }

    # =========================
    # REJECT FOLLOW REQUEST
    # =========================
    @staticmethod
    def reject_follow(target_user_id, requester_id):

        req = FollowRequest.query.filter_by(
            requester_id=requester_id,
            target_id=target_user_id
        ).first()

        if not req:
            return {"error": "Request not found"}, 404

        db.session.delete(req)
        db.session.commit()

        return {
            "message": "Follow request rejected",
            "status": "rejected",
            "follower_id": requester_id,
            "following_id": target_user_id
        }