from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.booking_service import BookingService
from app.schemas import BookingResponse


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/{city_id}")
def book_cab(city_id: int, db: Session = Depends(get_db)):
    """
    Books an available cab in the given city.
    If no cabs are available, returns an error message.
    """
    booking = BookingService.book_cab(db, city_id)
    if not booking:
        raise HTTPException(status_code=404, detail="No available cabs in this city")
    return {"message": "Cab booked successfully", "booking_id": booking.id, "cab_id": booking.cab_id}


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    """Fetches a city by its ID."""
    booking = BookingService.get_city_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/{booking_id}/complete", response_model=dict)
def complete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Marks a booking as completed by updating the drop time and setting the cab as IDLE.
    """
    booking = BookingService.complete_booking(db, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or already completed")

    return {"message": "Booking completed successfully", "booking_id": booking.id}



