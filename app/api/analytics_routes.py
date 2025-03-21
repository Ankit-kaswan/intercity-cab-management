from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/cab_idle_time/{cab_id}", response_model=dict)
def get_cab_idle_time(
        cab_id: int,
        start_time: datetime = Query(..., description="Start time in ISO format (YYYY-MM-DDTHH:MM:SS)"),
        end_time: datetime = Query(..., description="End time in ISO format (YYYY-MM-DDTHH:MM:SS)"),
        db: Session = Depends(get_db)
):
    """Gets total idle time of a cab within a given duration."""
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time")

    idle_time = AnalyticsService.get_cab_idle_time(db, cab_id, start_time, end_time)
    return {"idle_time": idle_time}


@router.get("/peak_demand/{city_id}", response_model=dict)
def get_peak_demand_hours(city_id: int, db: Session = Depends(get_db)):
    """Finds peak demand hours in a city."""
    peak_hours = AnalyticsService.get_peak_demand_hours(db, city_id)
    if peak_hours is None:
        raise HTTPException(status_code=404, detail="No booking data available for this city")

    return {"peak_hours": peak_hours}
