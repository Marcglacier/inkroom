from unittest.mock import patch

from app.infrastructure.celery.tasks import (
    send_verification_email_task,
)


def test_send_verification_email_task():
    email = "inkroom-test@example.com"
    verification_code = "123456"

    with patch(
        "app.infrastructure.celery.tasks.SendVerificationEmailService"
    ) as mock_service:

        result = send_verification_email_task.run(
            email=email,
            verification_code=verification_code,
        )

        mock_service.assert_called_once_with(
            email=email,
            verification_code=verification_code,
        )

        mock_service.return_value.execute.assert_called_once()

        assert result is None