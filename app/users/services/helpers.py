# app/users/services/helpers.py
def response(message, state, **extra):

    return {
        "message": message,
        "state": state,
        **extra
    }