# providers/agromonitoring_provider.py

import requests

from config import AGROMONITORING_API_KEY

from providers.utils import (
    standard_weather_structure,
    build_forecast_entry
)



def fetch_agromonitoring(lat, lon):
    url = (
        f"https://api.agromonitoring.com/agro/1.0/weather/forecast?"
        f"lat={lat}&lon={lon}&appid={AGROMONITORING_API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    forecast = []

    for item in data[:48]:
        forecast.append(
            build_forecast_entry(
                timestamp=item.get("dt"),
                rainfall=item.get("rain"),
                temperature=item.get("main", {}).get("temp"),
                humidity=item.get("main", {}).get("humidity"),
                pressure=item.get("main", {}).get("pressure"),
                wind_speed=item.get("wind", {}).get("speed"),
                wind_direction=item.get("wind", {}).get("deg")
            )
        )

    return standard_weather_structure(
        "Agromonitoring",
        lat,
        lon,
        forecast
    )