from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.state_machine import CabState
from app.repositories.cab_repository import CabRepository
from app.repositories.booking_repository import BookingRepository
from app.services.cab_service import CabService
from datetime import datetime
import random


class BookingService:
    @staticmethod
    def book_cab(db: Session, city_id: int):
        """
        Books an available cab based on idle time.
        - Fetches the longest idle cab using a single optimized DB query.
        - If multiple cabs have the same idle time, selects one randomly.
        - Updates the cab's status to `ON_TRIP` while ensuring transaction integrity.
        """

        available_cabs = CabRepository.get_available_cabs(db, city_id)

        if not available_cabs:
            raise HTTPException(status_code=404, detail="No available cabs in this city")

        # Identify cabs with the longest idle time
        longest_idle_time = available_cabs[0].last_idle_time
        longest_idle_cabs = [cab for cab in available_cabs if cab.last_idle_time == longest_idle_time]

        # Randomly select a cab if multiple have the same idle time
        assigned_cab = random.choice(longest_idle_cabs)

        try:
            # Create booking record (ensures cab status change is tied to a successful booking)
            booking = BookingRepository.create_booking(db, assigned_cab.id, city_id)

            # Use repository method to update cab state
            CabService.update_cab_state(db, booking.cab_id, CabState.ON_TRIP.value)

            db.commit()  # Commit transaction after both operations succeed
            db.refresh(booking)

            return booking

        except Exception as e:
            db.rollback()  # Rollback in case of failure
            raise HTTPException(status_code=500, detail="Failed to book cab")

    @staticmethod
    def get_city_by_id(db: Session, booking_id: int):
        """Fetches a booking by its ID."""
        return BookingRepository.get_booking_by_id(db, booking_id)

    @staticmethod
    def complete_booking(db: Session, booking_id: int):
        """
        Completes a booking by setting the drop time and marking the cab as IDLE.
        """
        try:
            # Fetch the booking
            booking = BookingRepository.get_booking_by_id(db, booking_id)
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")

            if booking.drop_time is not None:
                raise HTTPException(status_code=400, detail="Booking is already completed")

            # Update drop time
            booking.drop_time = datetime.utcnow()

            # Use repository method to update cab state
            CabService.update_cab_state(db, booking.cab_id, CabState.IDLE.value)

            # Commit changes
            db.commit()
            db.refresh(booking)
            return booking

        except HTTPException:
            raise  # Rethrow known HTTP exceptions

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
