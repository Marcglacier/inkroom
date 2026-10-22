# app/inbox/services/settings/blocks/block_service.py

from sqlalchemy import or_

from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.models.settings.user_block import UserBlock
from app.extensions import db, socketio
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.sockets.presence_store import user_connections
from app.inbox.services.presence.presence_events import (
    emit_presence_status,
)

class BlockService:
    @staticmethod
    def block(blocker_id, blocked_id):
        if blocker_id == blocked_id:
            return False

        existing = UserBlock.query.filter_by(
            blocker_id=blocker_id,
            blocked_id=blocked_id,
        ).first()

        if existing:
            BlockService._remove_shared_room_access(
                blocker_id,
                blocked_id,
            )
            return False

        try:
            db.session.add(
                UserBlock(
                    blocker_id=blocker_id,
                    blocked_id=blocked_id,
                )
            )

            BlockService._remove_relationships(
                blocker_id, blocked_id
            )
            db.session.commit()
            BlockService._emit_block_updated(
                blocker_id,
                blocked_id,
                True,
            )

            BlockService._remove_shared_room_access(
                blocker_id,
                blocked_id,
            )

            emit_presence_status(blocker_id, False)
            emit_presence_status(blocked_id, False)

            return True
        except Exception:
            db.session.rollback()
            raise
    @staticmethod
    def _emit_block_updated(blocker_id, blocked_id, is_blocked):
        payload = {
            "blocker_id": blocker_id,
            "blocked_id": blocked_id,
            "is_blocked": is_blocked,
        }

        for user_id in (blocker_id, blocked_id):
            socketio.emit(
                "user:block_updated",
                payload,
                room=f"user_{user_id}",
            )

    @staticmethod
    def unblock(blocker_id, blocked_id):
        block = UserBlock.query.filter_by(
            blocker_id=blocker_id,
            blocked_id=blocked_id,
        ).first()

        if not block:
            return False

        db.session.delete(block)
        db.session.commit()
        BlockService._emit_block_updated(
            blocker_id,
            blocked_id,
            False,
        )
        emit_presence_status(blocker_id, False)
        emit_presence_status(blocked_id, False)
        return True

    @staticmethod
    def _remove_shared_room_access(user_a_id, user_b_id):
        conversations_a = {
            row[0]
            for row in (
                db.session.query(
                    ConversationParticipant.conversation_id
                )
                .filter_by(user_id=user_a_id)
                .all()
            )
        }

        conversations_b = {
            row[0]
            for row in (
                db.session.query(
                    ConversationParticipant.conversation_id
                )
                .filter_by(user_id=user_b_id)
                .all()
            )
        }

        shared_conversations = conversations_a & conversations_b

        for conversation_id in shared_conversations:
            room = f"conversation_{conversation_id}"

            for user_id in (user_a_id, user_b_id):
                for sid in list(user_connections.get(user_id, set())):
                    socketio.server.leave_room(
                        sid,
                        room,
                        namespace="/",
                    )

    @staticmethod
    def _remove_relationships(user_a_id, user_b_id):
        directions = or_(
            (
                (Follow.follower_id == user_a_id)
                & (Follow.following_id == user_b_id)
            ),
            (
                (Follow.follower_id == user_b_id)
                & (Follow.following_id == user_a_id)
            ),
        )
        db.session.query(Follow).filter(directions).delete(
            synchronize_session=False
        )

        requests = or_(
            (
                (FollowRequest.requester_id == user_a_id)
                & (FollowRequest.target_id == user_b_id)
            ),
            (
                (FollowRequest.requester_id == user_b_id)
                & (FollowRequest.target_id == user_a_id)
            ),
        )
        db.session.query(FollowRequest).filter(requests).delete(
            synchronize_session=False
        )
