import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.schemas import CabResponse, CabHistoryResponse
from app.state_machine import CabState
from datetime import datetime

client = TestClient(app)


@patch("app.services.cab_service.CabService.register_cab")
def test_register_cab(mock_register_cab):
    """Test registering a new cab."""
    mock_register_cab.return_value = CabResponse(
        id=1,
        city_id=1,
        state=CabState.IDLE,
        plate_number="XYZ-123",
        current_city_id=1,
        last_idle_time=datetime.utcnow()
    )

    response = client.post("/cabs/", json={"current_city_id": 1, "plate_number": "XYZ-123"})

    assert response.status_code == 201
    assert response.json()["id"] == 1


@patch("app.services.city_service.CityService.register_city")
def test_register_city_failure(mock_register_city):
    """Test case when city registration fails unexpectedly."""

    mock_register_city.return_value = None  # Simulate failure

    city_data = {"name": "Delhi"}

    response = client.post("/cities/", json=city_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to register city."}


@patch("app.services.cab_service.CabService.change_cab_location")
def test_update_cab_location_success(mock_change_location):
    """Test updating cab location successfully."""
    mock_change_location.return_value = CabResponse(
        id=1,
        state=CabState.IDLE,
        plate_number="XYZ-123",
        current_city_id=2,
        last_idle_time=datetime.utcnow()
    )

    response = client.put("/cabs/1/location/2")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["state"] == "IDLE"
    assert response.json()["plate_number"] == "XYZ-123"
    assert response.json()["current_city_id"] == 2
    assert "last_idle_time" in response.json()


@patch("app.services.cab_service.CabService.change_cab_location")
def test_update_cab_location_not_found(mock_change_location):
    """Test updating cab location when cab not found."""
    mock_change_location.return_value = None

    response = client.put("/cabs/1/location/2")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cab not found"}


@patch("app.services.cab_service.CabService.update_cab_state")
def test_update_cab_state_success(mock_update_state):
    """Test updating cab state successfully."""
    mock_update_state.return_value = CabResponse(
        id=1,
        state=CabState.ON_TRIP,
        plate_number="XYZ-123",
        current_city_id=1,
        last_idle_time=datetime.utcnow()
    )
    response = client.put("/cabs/1/state/ON_TRIP")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["state"] == "ON_TRIP"
    assert response.json()["plate_number"] == "XYZ-123"
    assert response.json()["current_city_id"] == 1
    assert "last_idle_time" in response.json()


@patch("app.services.cab_service.CabService.update_cab_state")
def test_update_cab_state_not_found(mock_update_state):
    """Test updating cab state when cab is not found."""
    mock_update_state.return_value = None

    response = client.put("/cabs/1/state/ON_TRIP")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cab not found"}


@patch("app.services.cab_service.CabService.get_available_cabs")
def test_get_available_cabs(mock_get_available_cabs):
    """Test fetching available cabs."""
    mock_get_available_cabs.return_value = [
        CabResponse(
            id=1,
            city_id=1,
            state=CabState.IDLE,
            plate_number="XYZ-123",
            current_city_id=1,
            last_idle_time=datetime.utcnow()
        ),
        CabResponse(
            id=2,
            city_id=1,
            state=CabState.IDLE,
            plate_number="ABC-456",
            current_city_id=1,
            last_idle_time=datetime.utcnow()
        ),
    ]

    response = client.get("/cabs/available/1")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["state"] == "IDLE"
    assert response.json()[0]["plate_number"] == "XYZ-123"
    assert response.json()[1]["id"] == 2
    assert response.json()[1]["state"] == "IDLE"
    assert response.json()[1]["plate_number"] == "ABC-456"
    assert "last_idle_time" in response.json()[0]


@patch("app.services.cab_service.CabService.get_available_cabs")
def test_get_available_cabs_no_cabs(mock_get_available_cabs):
    """Test fetching available cabs when none exist."""
    mock_get_available_cabs.return_value = []

    response = client.get("/cabs/available/1")

    assert response.status_code == 200
    assert response.json() == []


@patch("app.services.cab_service.CabService.get_cab_history")
def test_get_cab_history(mock_get_cab_history):
    """Test fetching cab state change history."""
    mock_get_cab_history.return_value = [
        CabHistoryResponse(
            id=1,
            cab_id=1,
            state=CabState.IDLE,
            timestamp=datetime.utcnow().isoformat()
        ),
        CabHistoryResponse(
            id=2,
            cab_id=1,
            state=CabState.ON_TRIP,
            timestamp=datetime.utcnow().isoformat()
        ),
    ]

    response = client.get("/cabs/1/history")

    assert response.status_code == 200
    history = response.json()

    assert isinstance(history, list)
    assert len(history) == 2
    assert history[0]["id"] == 1
    assert history[0]["cab_id"] == 1
    assert history[0]["state"] == "IDLE"
    assert "timestamp" in history[0]
    assert history[1]["id"] == 2
    assert history[1]["cab_id"] == 1
    assert history[1]["state"] == "ON_TRIP"
    assert "timestamp" in history[1]
