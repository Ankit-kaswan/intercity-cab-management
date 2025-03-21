import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from app.main import app
from app.schemas import CityResponse
from app.repositories.city_repository import CityRepository

client = TestClient(app)


@patch("app.services.city_service.CityService.register_city")
def test_register_city_success(mock_register_city):
    """Test successful city registration."""
    mock_register_city.return_value = CityResponse(id=1, name="New York")

    response = client.post("/cities/", json={"name": "Delhi"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Delhi"}


@patch("app.services.city_service.CityService.register_city")
def test_register_city_duplicate(mock_register_city):
    """Test registering a duplicate city raises a 400 error."""
    mock_register_city.side_effect = IntegrityError("City already exists", params=None, orig=None)

    response = client.post("/cities/", json={"name": "Delhi"})

    assert response.status_code == 400
    assert response.json()["detail"] == "City with this name already exists."


@patch("app.services.city_service.CityService.get_all_cities")
def test_get_all_cities(mock_get_all_cities):
    """Test retrieving all cities."""
    mock_get_all_cities.return_value = [
        CityResponse(id=1, name="Delhi"),
        CityResponse(id=2, name="Mumbai"),
    ]

    response = client.get("/cities/")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Delhi"},
        {"id": 2, "name": "Mumbai"},
    ]


@patch("app.services.city_service.CityService.get_city_by_id")
def test_get_city_by_id_success(mock_get_city_by_id):
    """Test fetching a city by ID."""
    mock_get_city_by_id.return_value = CityResponse(id=1, name="Delhi")

    response = client.get("/cities/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Delhi"}


@patch("app.services.city_service.CityService.get_city_by_id")
def test_get_city_by_id_not_found(mock_get_city_by_id):
    """Test fetching a city by ID that does not exist."""
    mock_get_city_by_id.return_value = None

    response = client.get("/cities/99")

    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"


@patch("app.services.city_service.CityService.update_city")
def test_update_city_success(mock_update_city):
    """Test updating a city successfully."""
    mock_update_city.return_value = CityResponse(id=1, name="Delhi Updated")

    response = client.put("/cities/1", json={"name": "Delhi Updated"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Delhi Updated"}


@patch("app.services.city_service.CityService.update_city")
def test_update_city_failure(mock_update_city):
    """Test updating a city that does not exist."""
    mock_update_city.return_value = None

    response = client.put("/cities/99", json={"name": "Unknown City"})

    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"


@patch("app.services.city_service.CityService.delete_city")
def test_delete_city_success(mock_delete_city):
    """Test deleting a city successfully."""
    mock_delete_city.return_value = True

    response = client.delete("/cities/1")

    assert response.status_code == 200
    assert response.json() == {"message": "City deleted successfully"}


@patch("app.repositories.city_repository.CityRepository.delete_city")
def test_delete_city_not_found(mock_delete_city):
    print("TEST STARTED")  # Debugging
    mock_delete_city.return_value = None  # Simulate city not found

    response = client.delete("/cities/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "City not found"}


@patch("app.repositories.city_repository.Session")
def test_get_all_cities_empty(mock_session):
    """Test retrieving cities when no cities exist."""
    mock_db = mock_session.return_value
    mock_db.query.return_value.all.return_value = []

    result = CityRepository.get_all_cities(mock_db)

    assert result == []
