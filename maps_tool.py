"""
maps_tool.py — Google Maps Places API integration.
"""

import os
import requests


class MapsTool:
    GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    MAPS_BASE = "https://www.google.com/maps/search/?api=1"

    def __init__(self):
        self.api_key = os.environ["GOOGLE_MAPS_API_KEY"]

    def search_places(
        self,
        location: str,
        query: str,
        max_results: int = 5,
        min_rating: float = 3.5,
    ) -> dict:
        """Search for places by query near a location."""
        coords = self._geocode(location)

        params = {
            "query": f"{query} in {location}",
            "key": self.api_key,
        }
        if coords:
            params["location"] = f"{coords['lat']},{coords['lng']}"
            params["radius"] = 5000  # 5 km radius

        resp = requests.get(self.PLACES_URL, params=params, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results", [])

        places = []
        for place in results[:max_results]:
            rating = place.get("rating", 0)
            if rating < min_rating:
                continue

            place_id = place.get("place_id", "")
            maps_url = f"{self.MAPS_BASE}&query={requests.utils.quote(place['name'])}&query_place_id={place_id}"

            places.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": rating,
                "user_ratings_total": place.get("user_ratings_total", 0),
                "price_level": self._price_label(place.get("price_level")),
                "open_now": place.get("opening_hours", {}).get("open_now"),
                "maps_url": maps_url,
            })

        return {
            "query": query,
            "location": location,
            "results_count": len(places),
            "places": places,
        }

    def _geocode(self, location: str) -> dict | None:
        resp = requests.get(
            self.GEOCODE_URL,
            params={"address": location, "key": self.api_key},
            timeout=10,
        )
        data = resp.json()
        if data.get("results"):
            return data["results"][0]["geometry"]["location"]
        return None

    @staticmethod
    def _price_label(level: int | None) -> str:
        return {0: "Free", 1: "$", 2: "$$", 3: "$$$", 4: "$$$$"}.get(level, "Unknown")
