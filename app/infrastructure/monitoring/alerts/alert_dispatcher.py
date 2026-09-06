# app/infrastructure/monitoring/alerts/alert_dispatcher.py

import logging
from datetime import datetime, timezone

from flask import current_app, has_app_context
from flask_mail import Message

from app.extensions import mail


logger = logging.getLogger("inkroom.health")


class AlertDispatcher:

    def __init__(self):
        self.dispatched = []
        self.delivery_history = []

    def dispatch(
        self,
        alert: dict,
    ) -> dict:

        self.dispatched.append(alert)

        delivery = self._send_email(alert)

        delivery_record = {
            "alert": alert,
            "status": delivery["status"],
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        if "error" in delivery:
            delivery_record["error"] = delivery["error"]

        self.delivery_history.append(
            delivery_record
        )

        return alert

    def _send_email(
        self,
        alert: dict,
    ) -> dict:

        if not has_app_context():
            return {
                "status": "skipped",
            }

        recipient = current_app.config.get(
            "ALERT_EMAIL"
        )

        if not recipient:
            logger.warning(
                "Health alert email skipped: "
                "ALERT_EMAIL is not configured"
            )

            return {
                "status": "skipped",
            }

        try:
            message = Message(
                subject=(
                    "InkRoom Health Alert: "
                    f"{alert.get('status', 'unknown').upper()}"
                ),
                recipients=[recipient],
                body=(
                    "InkRoom health monitoring detected "
                    "an alert.\n\n"
                    f"Status: {alert.get('status')}\n"
                    f"Message: {alert.get('message')}\n\n"
                    "Health result:\n"
                    f"{alert.get('result')}"
                ),
            )

            mail.send(message)

            logger.info(
                "Health alert email dispatched | "
                "status=%s",
                alert.get("status"),
            )

            return {
                "status": "sent",
            }

        except Exception as exc:
            logger.exception(
                "Failed to dispatch health alert email"
            )

            return {
                "status": "failed",
                "error": str(exc),
            }

    def get_dispatched(self) -> list[dict]:

        return list(self.dispatched)

    def latest(self) -> dict | None:

        if not self.dispatched:
            return None

        return self.dispatched[-1]

    def get_delivery_history(self) -> list[dict]:

        return list(self.delivery_history)

    def latest_delivery(self) -> dict | None:

        if not self.delivery_history:
            return None

        return self.delivery_history[-1]

    def clear(self) -> None:

        self.dispatched.clear()
        self.delivery_history.clear()

