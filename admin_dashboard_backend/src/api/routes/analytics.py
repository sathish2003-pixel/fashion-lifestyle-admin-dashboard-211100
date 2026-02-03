"""
Analytics API routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.services import analytics as analytics_service
from src.auth import get_current_active_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/", response_model=schemas.AnalyticsResponse, summary="Get comprehensive analytics")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get comprehensive analytics including dashboard stats, revenue trends, and top products.
    
    Args:
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Complete analytics data
    """
    return analytics_service.get_analytics(db)


@router.get("/dashboard", response_model=schemas.DashboardStats, summary="Get dashboard statistics")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get dashboard statistics including totals and growth metrics.
    
    Args:
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Dashboard statistics
    """
    return analytics_service.get_dashboard_stats(db)
