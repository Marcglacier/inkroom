# app/inbox/services/calls/missed_call_monitor.py
import logging
import threading

from flask import Flask

from app.inbox.services.calls.expire_missed_calls_service import (
    ExpireMissedCallsService,
)


logger = logging.getLogger("inkroom.calls")


class MissedCallMonitor:

    def __init__(
        self,
        app: Flask,
        interval_seconds: int = 1,
    ):
        self.app = app
        self.interval_seconds = interval_seconds
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):

        if (
            self._thread
            and self._thread.is_alive()
        ):
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            name="inkroom-missed-call-monitor",
            daemon=True,
        )

        self._thread.start()

        logger.info(
            "Missed call monitor started | "
            "interval=%ss",
            self.interval_seconds,
        )

    def stop(self):

        self._stop_event.set()

        logger.info(
            "Missed call monitor stopped"
        )

    def _run(self):

        while not self._stop_event.is_set():

            self._check()

            self._stop_event.wait(
                self.interval_seconds
            )

    def _check(self):

        try:

            with self.app.app_context():

                expired = (
                    ExpireMissedCallsService()
                    .execute()
                )

            if expired:
                logger.info(
                    "Missed calls expired | "
                    "count=%s",
                    expired,
                )

        except Exception:

            logger.exception(
                "Automatic missed call expiry failed"
            )