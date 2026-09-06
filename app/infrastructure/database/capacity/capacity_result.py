# app/infrastructure/database/capacity/capacity_result.py

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapacityResult:

    status: str

    database: dict

    pool: dict

    pool_wait: dict