import requests

from config import TOMORROW_API_KEY

from providers.utils import (
    build_forecast_entry,
    standard_weather_structure
)


def fetch_tomorrow(lat, lon):

    url = "https://api.tomorrow.io/v4/weather/forecast"

    params = {
        "location": f"{lat},{lon}",
        "apikey": TOMORROW_API_KEY,
        "timesteps": "1h",
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("Tomorrow.io Status:", response.status_code)

    if response.status_code != 200:
        print("Tomorrow.io Error:")
        print(response.text[:500])

        return standard_weather_structure(
            "Tomorrow.io",
            lat,
            lon,
            []
        )

    data = response.json()

    forecast = []

    hourly = data.get(
        "timelines",
        {}
    ).get(
        "hourly",
        []
    )

    print("Tomorrow hourly records:", len(hourly))

    for item in hourly[:48]:

        values = item.get(
            "values",
            {}
        )

        forecast.append(

            build_forecast_entry(

                timestamp=item.get("time"),

                temperature=values.get(
                    "temperature"
                ),

                humidity=values.get(
                    "humidity"
                ),

                rainfall=values.get(
                    "rainIntensity"
                ),

                wind_speed=values.get(
                    "windSpeed"
                ),

                wind_direction=values.get(
                    "windDirection"
                ),

                pressure=values.get(
                    "pressureSurfaceLevel"
                ),

                cloud_cover=values.get(
                    "cloudCover"
                )

            )

        )

    print(
        "Tomorrow forecast created:",
        len(forecast)
    )

    if len(forecast) > 0:
        print(
            "Sample record:",
            forecast[0]
        )

    return standard_weather_structure(
        "Tomorrow.io",
        lat,
        lon,
        forecast
    )