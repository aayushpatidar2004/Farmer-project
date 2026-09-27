"""
Open-Meteo weather service integration.

Open-Meteo is completely free and requires NO API key.
Docs: https://open-meteo.com/en/docs
"""
import logging

import requests

logger = logging.getLogger(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10  # seconds

# WMO Weather Code Descriptions
# https://open-meteo.com/en/docs#weathervariables
WEATHER_CODE_MAP = {
    0: {"description": "Clear Sky", "icon": "bi-sun-fill", "bg": "warning"},
    1: {"description": "Mainly Clear", "icon": "bi-sun-fill", "bg": "warning"},
    2: {"description": "Partly Cloudy", "icon": "bi-cloud-sun-fill", "bg": "info"},
    3: {"description": "Overcast", "icon": "bi-clouds-fill", "bg": "secondary"},
    45: {"description": "Fog", "icon": "bi-cloud-fog-fill", "bg": "secondary"},
    48: {"description": "Depositing Rime Fog", "icon": "bi-cloud-fog-fill", "bg": "secondary"},
    51: {"description": "Light Drizzle", "icon": "bi-cloud-drizzle-fill", "bg": "info"},
    53: {"description": "Moderate Drizzle", "icon": "bi-cloud-drizzle-fill", "bg": "info"},
    55: {"description": "Dense Drizzle", "icon": "bi-cloud-drizzle-fill", "bg": "primary"},
    61: {"description": "Slight Rain", "icon": "bi-cloud-rain-fill", "bg": "primary"},
    63: {"description": "Moderate Rain", "icon": "bi-cloud-rain-fill", "bg": "primary"},
    65: {"description": "Heavy Rain", "icon": "bi-cloud-rain-heavy-fill", "bg": "danger"},
    71: {"description": "Slight Snow", "icon": "bi-cloud-snow-fill", "bg": "light"},
    73: {"description": "Moderate Snow", "icon": "bi-cloud-snow-fill", "bg": "light"},
    75: {"description": "Heavy Snow", "icon": "bi-cloud-snow-fill", "bg": "light"},
    77: {"description": "Snow Grains", "icon": "bi-cloud-snow-fill", "bg": "light"},
    80: {"description": "Slight Showers", "icon": "bi-cloud-rain-fill", "bg": "primary"},
    81: {"description": "Moderate Showers", "icon": "bi-cloud-rain-fill", "bg": "primary"},
    82: {"description": "Violent Showers", "icon": "bi-cloud-rain-heavy-fill", "bg": "danger"},
    85: {"description": "Slight Snow Showers", "icon": "bi-cloud-snow-fill", "bg": "light"},
    86: {"description": "Heavy Snow Showers", "icon": "bi-cloud-snow-fill", "bg": "light"},
    95: {"description": "Thunderstorm", "icon": "bi-cloud-lightning-rain-fill", "bg": "dark"},
    96: {"description": "Thunderstorm with Hail", "icon": "bi-cloud-lightning-rain-fill", "bg": "dark"},
    99: {"description": "Thunderstorm + Heavy Hail", "icon": "bi-cloud-lightning-rain-fill", "bg": "dark"},
}

DEFAULT_WEATHER_INFO = {"description": "Unknown", "icon": "bi-question-circle", "bg": "secondary"}


def geocode_city(city_name: str) -> dict | None:
    """
    Convert a city name to latitude/longitude via Open-Meteo Geocoding API.

    Returns a location dict or None on failure.
    """
    try:
        resp = requests.get(
            GEOCODING_URL,
            params={"name": city_name.strip(), "count": 1, "language": "en", "format": "json"},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("results"):
            r = data["results"][0]
            return {
                "latitude": r["latitude"],
                "longitude": r["longitude"],
                "name": r.get("name", city_name),
                "country": r.get("country", ""),
                "admin1": r.get("admin1", ""),
            }
        return None

    except requests.exceptions.Timeout:
        logger.warning("Geocoding API timed out for city: %s", city_name)
        return None
    except requests.exceptions.RequestException as exc:
        logger.error("Geocoding API error for '%s': %s", city_name, exc)
        return None


def fetch_weather(latitude: float, longitude: float) -> dict | None:
    """
    Fetch current weather conditions from Open-Meteo forecast API.

    Returns a weather dict or None on failure.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
        ],
        "timezone": "auto",
    }

    try:
        resp = requests.get(WEATHER_URL, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        code = current.get("weather_code", 0)
        info = WEATHER_CODE_MAP.get(code, DEFAULT_WEATHER_INFO)

        return {
            "temperature": round(float(current.get("temperature_2m", 0)), 1),
            "feels_like": round(float(current.get("apparent_temperature", 0)), 1),
            "humidity": int(current.get("relative_humidity_2m", 0)),
            "precipitation": round(float(current.get("precipitation", 0)), 2),
            "wind_speed": round(float(current.get("wind_speed_10m", 0)), 1),
            "wind_direction": int(current.get("wind_direction_10m", 0)),
            "weather_code": code,
            "description": info["description"],
            "icon": info["icon"],
            "icon_bg": info["bg"],
            "cloud_cover": int(current.get("cloud_cover", 0)),
            "pressure": round(float(current.get("pressure_msl", 0)), 1),
            "timezone": data.get("timezone", ""),
        }

    except requests.exceptions.Timeout:
        logger.warning("Weather API timed out for lat=%s lon=%s", latitude, longitude)
        return None
    except requests.exceptions.RequestException as exc:
        logger.error("Weather API error: %s", exc)
        return None


def get_weather_by_city(city_name: str) -> tuple:
    """
    High-level function: look up a city and return its current weather.

    Returns:
        (weather_dict, location_dict, error_message)
        On success: (weather, location, None)
        On failure: (None, location_or_None, error_string)
    """
    if not city_name or not city_name.strip():
        return None, None, "Please enter a city name."

    location = geocode_city(city_name)
    if not location:
        return (
            None, None,
            f"City '{city_name}' not found. Please check the spelling and try again.",
        )

    weather = fetch_weather(location["latitude"], location["longitude"])
    if not weather:
        return (
            None, location,
            "Weather data is temporarily unavailable. Please try again in a moment.",
        )

    return weather, location, None
