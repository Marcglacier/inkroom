# app/users/social/actions/relationship_actions.py

from app.users.social.services.follow_user import FollowUserService
from app.users.social.services.unfollow_user import UnfollowUserService
from app.users.social.services.accept_follow import AcceptFollowService
from app.users.social.services.reject_follow import RejectFollowService

from app.notifications.services import (
    create_follow_notification,
    create_follow_request_notification,
    create_follow_accept_notification,
)

from app.sockets.follow import emit_relationship_updates


def follow_relationship(viewer_id: int, target_id: int) -> str:
    """
    Orchestrates a follow action.

    Mutation services handle database state.
    This layer handles side effects:
        - notifications
        - realtime relationship updates
    """

    result = FollowUserService(
        viewer_id,
        target_id,
    ).execute()

    if result == "following":
        create_follow_notification(
            viewer_id,
            target_id,
        )

        emit_relationship_updates(
            viewer_id,
            target_id,
        )

    elif result == "requested":
        create_follow_request_notification(
            viewer_id,
            target_id,
        )

        emit_relationship_updates(
            viewer_id,
            target_id,
        )

    return result


def unfollow_relationship(viewer_id: int, target_id: int) -> str:
    """
    Orchestrates an unfollow action.
    """

    result = UnfollowUserService(
        viewer_id,
        target_id,
    ).execute()

    if result == "unfollowed":
        emit_relationship_updates(
            viewer_id,
            target_id,
        )

    return result


def accept_follow_relationship(
    user_id: int,
    requester_id: int,
) -> str:
    """
    Orchestrates accepting a follow request.

    user_id:
        The person accepting the request.

    requester_id:
        The person who originally requested the follow.
    """

    result = AcceptFollowService(
        user_id,
        requester_id,
    ).execute()

    if result == "accepted":
        create_follow_accept_notification(
            user_id,
            requester_id,
        )

        emit_relationship_updates(
            user_id,
            requester_id,
        )

    return result


def reject_follow_relationship(
    user_id: int,
    requester_id: int,
) -> str:
    """
    Orchestrates rejecting a follow request.
    """

    result = RejectFollowService(
        user_id,
        requester_id,
    ).execute()

    if result == "rejected":
        emit_relationship_updates(
            user_id,
            requester_id,
        )

    return result