from sqlalchemy.orm import Session
from sqlalchemy import text


class HealthService:
    def __init__(self, db: Session):
        self.db = db

    def check_database_health(self) -> bool:
        """
        Perform a simple database query to verify database connectivity
        """
        try:
            # Execute a simple query to test database connection
            result = self.db.execute(text("SELECT 1"))
            result.fetchone()
            return True
        except Exception:
            return False

    def get_health_status(self) -> dict:
        """
        Get comprehensive health status including database connectivity
        """
        db_healthy = self.check_database_health()

        return {
            "status": "healthy" if db_healthy else "unhealthy",
            "database": "connected" if db_healthy else "disconnected",
            "message": (
                "All systems operational"
                if db_healthy
                else "Database connection failed"
            ),
        }
