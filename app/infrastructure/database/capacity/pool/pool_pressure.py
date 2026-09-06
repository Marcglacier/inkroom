# app/infrastructure/database/capacity/pool_pressure.py


class PoolPressure:

    @staticmethod
    def calculate(
        checked_out: int | None,
        max_capacity: int | None,
    ) -> float | None:

        if (
            checked_out is None
            or max_capacity is None
            or max_capacity <= 0
        ):
            return None

        return (
            checked_out
            / max_capacity
        )


