"""
weather_tool.py — OpenWeatherMap integration.
"""

import os
import requests
from dataclasses import dataclass


class WeatherTool:
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self):
        self.api_key = os.environ["OPENWEATHERMAP_API_KEY"]

    def get_weather(self, location: str, units: str = "metric") -> dict:
        """Get current weather and forecast for a location."""
        params = {"q": location, "appid": self.api_key, "units": units}

        current_resp = requests.get(f"{self.BASE_URL}/weather", params=params, timeout=10)
        current_resp.raise_for_status()
        current = current_resp.json()

        forecast_resp = requests.get(f"{self.BASE_URL}/forecast", params=params, timeout=10)
        forecast_resp.raise_for_status()
        forecast_items = forecast_resp.json()["list"][:3]

        unit_symbol = "°C" if units == "metric" else "°F"
        condition = current["weather"][0]["description"]
        is_outdoor_ok = self._is_outdoor_ok(current["weather"][0]["id"])

        return {
            "location": f"{current['name']}, {current['sys']['country']}",
            "temperature": f"{current['main']['temp']:.1f}{unit_symbol}",
            "feels_like": f"{current['main']['feels_like']:.1f}{unit_symbol}",
            "condition": condition,
            "humidity": f"{current['main']['humidity']}%",
            "wind_speed": f"{current['wind']['speed']} {'m/s' if units == 'metric' else 'mph'}",
            "outdoor_activities_advisable": is_outdoor_ok,
            "forecast_next_9h": [
                {
                    "time": item["dt_txt"],
                    "condition": item["weather"][0]["description"],
                    "temp": f"{item['main']['temp']:.1f}{unit_symbol}",
                }
                for item in forecast_items
            ],
        }

    @staticmethod
    def _is_outdoor_ok(weather_id: int) -> bool:
        """
        OpenWeatherMap condition codes:
        2xx = Thunderstorm, 3xx = Drizzle, 5xx = Rain, 6xx = Snow, 7xx = Atmosphere
        8xx = Clear/Clouds (mostly fine outdoors)
        """
        if 200 <= weather_id < 700:
            return False  # precipitation or storms
        return True
