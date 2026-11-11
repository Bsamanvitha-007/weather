import requests

from providers.utils import (
    build_forecast_entry,
    standard_weather_structure
)


def fetch_ecmwf(lat, lon):

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,"
        f"relative_humidity_2m,"
        f"precipitation,"
        f"wind_speed_10m,"
        f"surface_pressure"
        f"&models=ecmwf_ifs04"
        f"&forecast_days=2"
    )

    response = requests.get(url)

    data = response.json()

    hourly = data.get("hourly", {})

    forecast = []

    for i in range(min(48, len(hourly["time"]))):

        forecast.append(
            build_forecast_entry(
                timestamp=hourly["time"][i],
                rainfall=hourly["precipitation"][i],
                temperature=hourly["temperature_2m"][i],
                humidity=hourly["relative_humidity_2m"][i],
                wind_speed=hourly["wind_speed_10m"][i],
                pressure=hourly["surface_pressure"][i]
            )
        )

    return standard_weather_structure(
        "ECMWF",
        lat,
        lon,
        forecast
    )