from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.health_service import HealthService


router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies database connectivity
    """
    health_service = HealthService(db)
    health_status = health_service.get_health_status()

    return health_status


@router.get("/")
async def root(db: Session = Depends(get_db)):
    """
    Root endpoint for basic health check
    """
    health_service = HealthService(db)
    health_status = health_service.get_health_status()

    return {"message": "Daydream2 API is running!", **health_status}
