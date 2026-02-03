"""
Analytics service for dashboard statistics and reporting.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from src import models, schemas


# PUBLIC_INTERFACE
def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    """
    Get dashboard statistics.
    
    Args:
        db: Database session
        
    Returns:
        Dashboard statistics
    """
    # Total revenue
    total_revenue = db.query(func.sum(models.Order.total_amount)).scalar() or 0.0
    
    # Total orders
    total_orders = db.query(func.count(models.Order.id)).scalar() or 0
    
    # Total customers
    total_customers = db.query(func.count(models.Customer.id)).scalar() or 0
    
    # Total products
    total_products = db.query(func.count(models.Product.id)).scalar() or 0
    
    # Average order value
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    
    # Revenue growth (compare last 30 days to previous 30 days)
    now = datetime.utcnow()
    last_30_days = now - timedelta(days=30)
    prev_30_days = now - timedelta(days=60)
    
    current_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.created_at >= last_30_days
    ).scalar() or 0.0
    
    previous_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.created_at >= prev_30_days,
        models.Order.created_at < last_30_days
    ).scalar() or 0.0
    
    revenue_growth = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0.0
    
    # Orders growth
    current_orders = db.query(func.count(models.Order.id)).filter(
        models.Order.created_at >= last_30_days
    ).scalar() or 0
    
    previous_orders = db.query(func.count(models.Order.id)).filter(
        models.Order.created_at >= prev_30_days,
        models.Order.created_at < last_30_days
    ).scalar() or 0
    
    orders_growth = ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0.0
    
    return schemas.DashboardStats(
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_customers=total_customers,
        total_products=total_products,
        avg_order_value=avg_order_value,
        revenue_growth=revenue_growth,
        orders_growth=orders_growth
    )


# PUBLIC_INTERFACE
def get_revenue_by_day(db: Session, days: int = 30) -> List[schemas.RevenueByPeriod]:
    """
    Get revenue aggregated by day.
    
    Args:
        db: Database session
        days: Number of days to look back
        
    Returns:
        List of revenue by period
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        func.date(models.Order.created_at).label('period'),
        func.sum(models.Order.total_amount).label('revenue'),
        func.count(models.Order.id).label('orders')
    ).filter(
        models.Order.created_at >= start_date
    ).group_by(
        func.date(models.Order.created_at)
    ).order_by(
        func.date(models.Order.created_at)
    ).all()
    
    return [
        schemas.RevenueByPeriod(
            period=str(result.period),
            revenue=float(result.revenue or 0),
            orders=result.orders
        )
        for result in results
    ]


# PUBLIC_INTERFACE
def get_top_products(db: Session, limit: int = 10) -> List[schemas.TopProduct]:
    """
    Get top selling products.
    
    Args:
        db: Database session
        limit: Number of top products to return
        
    Returns:
        List of top products
    """
    results = db.query(
        models.Product.id,
        models.Product.name,
        func.sum(models.OrderItem.quantity).label('total_sold'),
        func.sum(models.OrderItem.total_price).label('total_revenue')
    ).join(
        models.OrderItem, models.Product.id == models.OrderItem.product_id
    ).group_by(
        models.Product.id, models.Product.name
    ).order_by(
        func.sum(models.OrderItem.total_price).desc()
    ).limit(limit).all()
    
    return [
        schemas.TopProduct(
            product_id=result.id,
            product_name=result.name,
            total_sold=int(result.total_sold or 0),
            total_revenue=float(result.total_revenue or 0)
        )
        for result in results
    ]


# PUBLIC_INTERFACE
def get_analytics(db: Session) -> schemas.AnalyticsResponse:
    """
    Get comprehensive analytics data.
    
    Args:
        db: Database session
        
    Returns:
        Complete analytics response
    """
    return schemas.AnalyticsResponse(
        dashboard_stats=get_dashboard_stats(db),
        revenue_by_day=get_revenue_by_day(db),
        top_products=get_top_products(db)
    )
