# app/users/services/helpers.py
def response(message, status, **extra):

    return {
        "message": message,
        "status": status,
        **extra
    }