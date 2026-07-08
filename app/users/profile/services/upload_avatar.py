from app.extensions import db
from app.storage.folders import avatar_folder
from app.storage.service import upload_file


def upload_avatar(user, file):
    result = upload_file(
        file=file,
        folder=avatar_folder(user.id),
    )

    user.profile_picture = result["object_key"]

    db.session.commit()

    return {
        "profile_picture": user.profile_picture,
    }