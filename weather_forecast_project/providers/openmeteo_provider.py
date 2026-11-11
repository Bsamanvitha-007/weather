# providers/openmeteo_provider.py

import requests
from providers.utils import (
    standard_weather_structure,
    build_forecast_entry
)


def fetch_openmeteo(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m,"
        f"precipitation,wind_speed_10m,cloud_cover,surface_pressure"
        f"&forecast_days=2"
    )

    response = requests.get(url)
    data = response.json()

    hourly = data.get("hourly", {})

    times = hourly.get("time", [])

    forecast = []

    for i in range(min(48, len(times))):
        forecast.append(
            build_forecast_entry(
                timestamp=times[i],
                rainfall=hourly.get("precipitation", [None])[i],
                temperature=hourly.get("temperature_2m", [None])[i],
                humidity=hourly.get("relative_humidity_2m", [None])[i],
                wind_speed=hourly.get("wind_speed_10m", [None])[i],
                pressure=hourly.get("surface_pressure", [None])[i],
                cloud_cover=hourly.get("cloud_cover", [None])[i]
            )
        )

    return standard_weather_structure(
        "Open-Meteo",
        lat,
        lon,
        forecast
    )