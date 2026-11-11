import requests

from config import OPENWEATHER_API_KEY

from providers.utils import (
    build_forecast_entry,
    standard_weather_structure
)


def fetch_openweather(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={lon}"
        f"&appid={OPENWEATHER_API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)

    data = response.json()

    forecast = []

    for item in data.get("list", [])[:16]:

        rain = 0

        if "rain" in item:
            rain = item["rain"].get("3h", 0)

        forecast.append(
            build_forecast_entry(
                timestamp=item.get("dt_txt"),
                rainfall=rain,
                temperature=item["main"].get("temp"),
                humidity=item["main"].get("humidity"),
                pressure=item["main"].get("pressure"),
                wind_speed=item["wind"].get("speed"),
                wind_direction=item["wind"].get("deg"),
                cloud_cover=item["clouds"].get("all")
            )
        )

    return standard_weather_structure(
        "OpenWeatherMap",
        lat,
        lon,
        forecast
    )