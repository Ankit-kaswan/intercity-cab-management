from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app

client = TestClient(app)


@patch("app.services.booking_service.BookingService.book_cab")
def test_book_cab_success(mock_book_cab):
    """Test booking a cab successfully."""
    mock_book_cab.return_value = MagicMock(id=1, cab_id=101)

    response = client.post("/bookings/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Cab booked successfully", "booking_id": 1, "cab_id": 101}


@patch("app.services.booking_service.BookingService.book_cab")
def test_book_cab_no_available_cabs(mock_book_cab):
    """Test booking a cab when no cabs are available."""
    mock_book_cab.return_value = None  # Simulate no cabs available

    response = client.post("/bookings/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "No available cabs in this city"}


@patch("app.services.booking_service.BookingService.get_city_by_id")
def test_get_booking_by_id_success(mock_get_booking_by_id):
    """Test fetching a booking by ID successfully."""
    mock_get_booking_by_id.return_value = MagicMock(
        id=1,
        cab_id=101,
        city_id=1,
        pickup_time=datetime.utcnow(),
        drop_time=None,
        created_at=datetime.utcnow(),
    )

    response = client.get("/bookings/1")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["cab_id"] == 101
    assert data["city_id"] == 1
    assert data["drop_time"] is None
    assert "pickup_time" in data
    assert "created_at" in data


@patch("app.services.booking_service.BookingService.get_city_by_id")
def test_get_booking_by_id_not_found(mock_get_booking_by_id):
    """Test fetching a booking that does not exist."""
    mock_get_booking_by_id.return_value = None

    response = client.get("/bookings/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}


@patch("app.services.booking_service.BookingService.complete_booking")
def test_complete_booking_success(mock_complete_booking):
    """Test completing a booking successfully."""
    mock_complete_booking.return_value = MagicMock(id=1)

    response = client.post("/bookings/1/complete")

    assert response.status_code == 200
    assert response.json() == {"message": "Booking completed successfully", "booking_id": 1}


@patch("app.services.booking_service.BookingService.complete_booking")
def test_complete_booking_not_found(mock_complete_booking):
    """Test completing a booking that does not exist or is already completed."""
    mock_complete_booking.return_value = None

    response = client.post("/bookings/1/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found or already completed"}
