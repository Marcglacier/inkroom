# app/inbox/services/messages/delete_message.py
from app.extensions import db


def delete_for_me(message, user_id):

    if not message.deleted_for_users:
        message.deleted_for_users = []

    if user_id not in message.deleted_for_users:
        message.deleted_for_users.append(user_id)

    db.session.commit()


def delete_for_everyone(message):

    message.deleted_for_everyone = True
    message.content = ""

    db.session.commit()


def undo_delete(message):

    message.deleted_for_everyone = False

    db.session.commit()

    return message