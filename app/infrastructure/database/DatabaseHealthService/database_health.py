# app/infrastructure/database/DatabaseHealthService/database_health.py
from .DatabaseConnectionChecker import (
    DatabaseConnectionChecker, )


class DatabaseHealth:

    def __init__(
        self,
        connection_checker=None,
    ):

        self.connection_checker = (
            connection_checker
            or DatabaseConnectionChecker()
        )

    def check(self) -> bool:

        return self.connection_checker.check()