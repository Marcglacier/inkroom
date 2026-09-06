# app/infrastructure/database/DatabaseHealthService/DatabaseConnectionChecker.py
import logging

from sqlalchemy import text

from app.extensions import db


logger = logging.getLogger("inkroom.database")


class DatabaseConnectionChecker:

    @staticmethod
    def check() -> bool:

        try:
            db.session.execute(
                text("SELECT 1")
            )

            return True

        except Exception:

            db.session.rollback()

            logger.exception(
                "Database connection check failed"
            )

            return False