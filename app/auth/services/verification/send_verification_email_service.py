# app/auth/services/verification/send_verification_email_service.py
from flask_mail import Message as MailMessage

from app.extensions import mail


class SendVerificationEmailService:

    SENDER = "InkRoom <noreply@inkroom.app>"

    def __init__(
        self,
        email: str,
        verification_code: str,
    ):
        self.email = email
        self.verification_code = verification_code

    def execute(self):

        message = MailMessage(
            subject="InkRoom Verification Code",
            sender=self.SENDER,
            recipients=[self.email],
            body=(
                "Greetings from the InkRoom.\n\n"
                "Your verification code is:\n\n"
                f"{self.verification_code}\n\n"
                "This code expires in 10 minutes.\n\n"
                "If you did not create an InkRoom account, "
                "you can safely ignore this email."
            ),
        )

        mail.send(message)