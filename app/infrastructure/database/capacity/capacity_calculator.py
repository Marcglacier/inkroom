# CapacityCalculator

class CapacityCalculator:

    @staticmethod
    def calculate(
        current: int | None,
        maximum: int | None,
    ) -> float | None:

        if (
            current is None
            or maximum is None
            or maximum <= 0
        ):
            return None

        return current / maximum

    @staticmethod
    def percentage(
        utilization: float | None,
    ) -> float | None:

        if utilization is None:
            return None

        return round(
            utilization * 100,
            2,
        )