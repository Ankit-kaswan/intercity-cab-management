from sqlalchemy.orm import Session
from app.models import Booking
from datetime import datetime
from app.repositories.cab_repository import CabRepository


class BookingRepository:
    @staticmethod
    def create_booking(db: Session, cab_id: int, city_id: int):
        """
        Creates a new booking and updates the cab status via `CabRepository.update_cab_state()`
        to maintain separation of concerns.
        """
        try:
            # Create booking record
            booking = Booking(cab_id=cab_id, city_id=city_id)
            db.add(booking)

            # Commit transaction
            db.commit()
            db.refresh(booking)
            return booking

        except Exception as e:
            db.rollback()  # Rollback in case of failure
            raise e

    @staticmethod
    def get_booking_by_id(db: Session, booking_id: int):
        """Fetches a booking by its ID."""
        return db.query(Booking).filter(Booking.id == booking_id).first()

    @staticmethod
    def complete_booking(db: Session, booking_id: int):
        """
        Completes an active booking by setting the drop time and marking the cab as IDLE.
        """
        return BookingRepository.complete_booking(db, booking_id)

    @staticmethod
    def analyze_peak_demand(db: Session, city_id: int):
        """Finds peak hours for cab demand."""
        bookings = db.query(Booking).filter(Booking.city_id == city_id).all()
        hourly_count = {}
        for booking in bookings:
            hour = booking.pickup_time.hour
            hourly_count[hour] = hourly_count.get(hour, 0) + 1
        return max(hourly_count, key=hourly_count.get) if hourly_count else None

