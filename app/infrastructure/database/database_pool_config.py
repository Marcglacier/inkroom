# app/infrastructure/database/database_pool_config.py
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabasePoolConfig:

    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int

    @property
    def max_capacity(self) -> int:

        return (
            self.pool_size
            + self.max_overflow
        )