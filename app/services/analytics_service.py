from sqlalchemy.orm import Session
from app.repositories.booking_repository import BookingRepository
from app.repositories.cab_repository import CabRepository
from datetime import datetime, timedelta


class AnalyticsService:
    @staticmethod
    def get_cab_idle_time(db: Session, cab_id: int, start_time: datetime, end_time: datetime):
        """Calculates total idle time of a cab within a given duration."""
        return CabRepository.get_idle_time(db, cab_id, start_time, end_time)

    @staticmethod
    def get_peak_demand_hours(db: Session, city_id: int):
        """Finds peak hours for cab demand in a city."""
        return BookingRepository.analyze_peak_demand(db, city_id)
