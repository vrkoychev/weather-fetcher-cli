import pytest
import requests
from unittest.mock import patch, Mock
from weather_fetcher import get_coordinates_for_city, get_current_weather

# Test for successful geocoding
@patch('weather_fetcher.requests.get')
def test_get_coordinates_for_city_success(mock_get):
    """Test successfully getting coordinates for a city."""
    # 1. Arrange
    mock_response = Mock()
    # .json() should return a dictionary our function understands
    mock_response.json.return_value = {
        'results': [
            {'name': 'Sofia', 'latitude': 42.6979, 'longitude': 23.3217}
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # 2. Act
    result = get_coordinates_for_city("Sofia")

    # 3. Assert
    assert result is not None
    assert result['latitude'] == 42.6979
    assert result['longitude'] == 23.3217
    mock_get.assert_called_once()

# Test for city not found
@patch('weather_fetcher.requests.get')
def test_get_coordinates_for_city_not_found(mock_get):
    """Test handling of a city that doesn't exist."""
    # 1. Arrange
    mock_response = Mock()
    mock_response.json.return_value = {'results': []}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # 2. Act
    result = get_coordinates_for_city("NonexistentCity")

    # 3. Assert
    assert result is None
    mock_get.assert_called_once()

# Test for network error during geocoding
@patch('weather_fetcher.requests.get')
def test_get_coordinates_network_error(mock_get):
    """Test handling of a network error (e.g., no internet)."""
    # 1. Arrange
    mock_get.side_effect = requests.exceptions.ConnectionError("Network problem")

    # 2. Act
    result = get_coordinates_for_city("Sofia")

    # 3. Assert
    assert result is None

# Test for successful weather fetch
@patch('weather_fetcher.requests.get')
def test_get_current_weather_success(mock_get):
    """Test successfully getting weather data."""
    # 1. Arrange
    mock_response = Mock()
    mock_response.json.return_value = {
        'current_weather': {'temperature': 15.5, 'windspeed': 10.2}
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # 2. Act
    result = get_current_weather(42.6979, 23.3217)

    # 3. Act
    assert result is not None
    assert result['temperature'] == 15.5
    mock_get.assert_called_once()