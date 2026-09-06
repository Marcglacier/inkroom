
# app/infrastructure/database/capacity/pool/pool_availability.py


class PoolAvailability:

    @staticmethod
    def calculate(
        checked_out: int | None,
        max_capacity: int | None,
    ) -> int | None:

        if (
            checked_out is None
            or max_capacity is None
        ):
            return None

        return max(
            max_capacity - checked_out,
            0,
        )

