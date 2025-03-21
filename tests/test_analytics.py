from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app

client = TestClient(app)


@patch("app.services.analytics_service.AnalyticsService.get_cab_idle_time")
def test_get_cab_idle_time_success(mock_get_cab_idle_time):
    """Test fetching cab idle time successfully."""
    mock_get_cab_idle_time.return_value = 120  # Idle time in minutes

    start_time = "2025-03-06T10:00:00"
    end_time = "2025-03-06T12:00:00"

    response = client.get(f"/analytics/cab_idle_time/1?start_time={start_time}&end_time={end_time}")

    assert response.status_code == 200
    assert response.json() == {"idle_time": 120}


@patch("app.services.analytics_service.AnalyticsService.get_peak_demand_hours")
def test_get_peak_demand_hours_success(mock_get_peak_demand_hours):
    """Test fetching peak demand hours successfully."""
    mock_get_peak_demand_hours.return_value = [18, 19, 20]  # Peak hours in a city

    response = client.get("/analytics/peak_demand/1")

    assert response.status_code == 200
    assert response.json() == {"peak_hours": [18, 19, 20]}


@patch("app.services.analytics_service.AnalyticsService.get_cab_idle_time")
def test_get_cab_idle_time_invalid_time(mock_get_cab_idle_time):
    """Test cab idle time with invalid time range (start_time >= end_time)."""
    start_time = "2025-03-06T12:00:00"
    end_time = "2025-03-06T10:00:00"

    response = client.get(f"/analytics/cab_idle_time/1?start_time={start_time}&end_time={end_time}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Start time must be before end time"}


@patch("app.services.analytics_service.AnalyticsService.get_peak_demand_hours")
def test_get_peak_demand_hours_not_found(mock_get_peak_demand_hours):
    """Test peak demand hours when no data is available."""
    mock_get_peak_demand_hours.return_value = None

    response = client.get("/analytics/peak_demand/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "No booking data available for this city"}
