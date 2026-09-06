# app/infrastructure/database/database_capacity_service.py

from .metrics import (
    DatabaseMetrics,
    DatabasePoolMetrics, DatabasePoolWaitMetrics
)

from .capacity import (
    CapacityCalculator, CapacityStatus, CapacityResult, 
    PoolPressure, PoolAvailability, PoolWaitStatus
)


class DatabaseCapacityService:

    def __init__(self):

        self.database_metrics = ( DatabaseMetrics() )
        self.pool_metrics = ( DatabasePoolMetrics() )
        self.pool_wait_metrics = ( DatabasePoolWaitMetrics() )
        

    def check(self) -> dict:

        database = (
            self.database_metrics
            .get_connection_metrics()
        )

        pool = (  self.pool_metrics 
                .get_pool_metrics() 
                )
        
        pool_wait = ( 
            self.pool_wait_metrics 
            .measure() 
            )
        
        pool_wait_status = ( 
            PoolWaitStatus.determine(
                pool_wait.get("wait_time_ms")
            )
        )
        pool_wait["status"] = pool_wait_status

        pool["available_capacity"] = PoolAvailability.calculate(
            pool["checked_out"],
            pool["max_capacity"],
        )

        database_utilization = (
            CapacityCalculator.calculate(
                database[
                    "current_connections"
                ],
                database[
                    "max_connections"
                ],
            )
        )

        pool_utilization = PoolPressure.calculate(
            pool["checked_out"],
            pool["max_capacity"],
        )

        database[
            "utilization"
        ] = CapacityCalculator.percentage(
            database_utilization
        )

        pool[
            "utilization"
        ] = CapacityCalculator.percentage(
            pool_utilization
        )

        status = CapacityStatus.determine(
            database_utilization,
            pool_utilization,
            pool_wait_status=pool_wait_status,
        )

        result = CapacityResult(
            status=status,
            database=database,
            pool=pool,
            pool_wait=pool_wait,
        )

        return {
            "status": result.status,
            "database": result.database,
            "pool": result.pool,
            "pool_wait": result.pool_wait,
        }

