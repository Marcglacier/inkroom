# app/notifications/services/utils.py
def should_notify(actor_id, user_id):
    return actor_id != user_id