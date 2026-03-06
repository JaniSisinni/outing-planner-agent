"""
tool_registry.py — Tool definitions passed to Claude's API.
"""

TOOL_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": (
            "Get current weather conditions and a short forecast for a given location. "
            "Returns temperature, condition (sunny/cloudy/rainy/etc.), wind, humidity, "
            "and whether outdoor activities are advisable."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or 'city,country_code' e.g. 'London,GB' or 'Austin,TX,US'",
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": "Temperature units. Default: metric (Celsius).",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "search_places",
        "description": (
            "Search for nearby places (restaurants, bars, parks, museums, etc.) "
            "using Google Maps Places API. Returns a list of places with name, "
            "address, rating, price level, and Maps URL."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City or address to search near.",
                },
                "query": {
                    "type": "string",
                    "description": "What to search for, e.g. 'rooftop bar', 'family park', 'cheap sushi restaurant'.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Max number of results to return (1-10). Default: 5.",
                    "default": 5,
                },
                "min_rating": {
                    "type": "number",
                    "description": "Minimum Google rating (0-5). Default: 3.5.",
                    "default": 3.5,
                },
            },
            "required": ["location", "query"],
        },
    },
]
