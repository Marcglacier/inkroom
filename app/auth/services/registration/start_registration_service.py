# app/auth/services/registration/start_registration_service.py
from app.auth.services.registration.register_user_service import (
    RegisterUserService,
)

from app.infrastructure.celery.tasks import (
    send_verification_email_task,
)

class StartRegistrationService:

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        is_private: bool = False,
    ):
        self.username = username
        self.email = email
        self.password = password
        self.is_private = bool(is_private)

    def execute(self):

        # ================= CREATE PENDING REGISTRATION =================

        result = RegisterUserService(
            username=self.username,
            email=self.email,
            password=self.password,
            is_private=self.is_private,
        ).execute()

        # ================= SEND VERIFICATION EMAIL =================

        send_verification_email_task.delay(
            email=result["email"],
            verification_code=result["verification_code"],
        )

        # ================= RESPONSE DATA =================

        return {
            "email": result["email"],
            "username": result["username"],
            "requires_verification": True,
        }