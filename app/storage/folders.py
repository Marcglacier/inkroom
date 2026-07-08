def avatar_folder(user_id: int) -> str:
    return f"avatars/{user_id}"


def chat_folder(conversation_id: int) -> str:
    return f"chat/{conversation_id}"


def voice_folder(conversation_id: int) -> str:
    return f"voice/{conversation_id}"


def file_folder(conversation_id: int) -> str:
    return f"files/{conversation_id}"


def story_folder(user_id: int) -> str:
    return f"stories/{user_id}"