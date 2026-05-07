# app/inbox/services/messages/edit_message.py
from app.extensions import db


def edit_message(message, new_content):

    message.content = new_content
    message.edited = True

    db.session.commit()
    return message