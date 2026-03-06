"""
test_weather_tool.py — Unit tests for the WeatherTool.
"""

import pytest
from unittest.mock import patch, MagicMock
from tools.weather_tool import WeatherTool


MOCK_CURRENT = {
    "name": "Austin",
    "sys": {"country": "US"},
    "main": {"temp": 28.0, "feels_like": 30.0, "humidity": 55},
    "wind": {"speed": 3.5},
    "weather": [{"id": 800, "description": "clear sky"}],
}

MOCK_FORECAST = {
    "list": [
        {"dt_txt": "2024-06-01 15:00:00", "main": {"temp": 29.0}, "weather": [{"description": "clear sky"}]},
        {"dt_txt": "2024-06-01 18:00:00", "main": {"temp": 27.0}, "weather": [{"description": "few clouds"}]},
        {"dt_txt": "2024-06-01 21:00:00", "main": {"temp": 25.0}, "weather": [{"description": "clear sky"}]},
    ]
}


@pytest.fixture
def weather_tool(monkeypatch):
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "fake-key")
    return WeatherTool()


@patch("tools.weather_tool.requests.get")
def test_get_weather_sunny(mock_get, weather_tool):
    responses = [MagicMock(), MagicMock()]
    responses[0].json.return_value = MOCK_CURRENT
    responses[1].json.return_value = MOCK_FORECAST
    for r in responses:
        r.raise_for_status = MagicMock()
    mock_get.side_effect = responses

    result = weather_tool.get_weather("Austin,US")

    assert result["location"] == "Austin, US"
    assert result["condition"] == "clear sky"
    assert result["outdoor_activities_advisable"] is True
    assert len(result["forecast_next_9h"]) == 3


@patch("tools.weather_tool.requests.get")
def test_get_weather_rainy_blocks_outdoor(mock_get, weather_tool):
    rainy_current = {**MOCK_CURRENT, "weather": [{"id": 502, "description": "heavy intensity rain"}]}
    responses = [MagicMock(), MagicMock()]
    responses[0].json.return_value = rainy_current
    responses[1].json.return_value = MOCK_FORECAST
    for r in responses:
        r.raise_for_status = MagicMock()
    mock_get.side_effect = responses

    result = weather_tool.get_weather("Austin,US")
    assert result["outdoor_activities_advisable"] is False


def test_is_outdoor_ok_thresholds():
    assert WeatherTool._is_outdoor_ok(800) is True   # clear sky
    assert WeatherTool._is_outdoor_ok(801) is True   # few clouds
    assert WeatherTool._is_outdoor_ok(500) is False  # light rain
    assert WeatherTool._is_outdoor_ok(200) is False  # thunderstorm
    assert WeatherTool._is_outdoor_ok(601) is False  # snow
