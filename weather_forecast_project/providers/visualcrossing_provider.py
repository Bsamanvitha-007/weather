# providers/visualcrossing_provider.py

import requests

from config import VISUALCROSSING_API_KEY

from providers.utils import (
    standard_weather_structure,
    build_forecast_entry
)


def fetch_visualcrossing(lat, lon):

    url = (
        f"https://weather.visualcrossing.com/"
        f"VisualCrossingWebServices/rest/services/timeline/"
        f"{lat},{lon}"
        f"?unitGroup=metric"
        f"&include=hours"
        f"&key={VISUALCROSSING_API_KEY}"
        f"&contentType=json"
    )

    response = requests.get(url)

    data = response.json()

    forecast = []

    count = 0

    for day in data.get("days", []):

        for hour in day.get("hours", []):

            if count >= 48:
                break

            forecast.append(

                build_forecast_entry(

                    timestamp=hour.get("datetime"),

                    rainfall=hour.get("precip"),

                    temperature=hour.get("temp"),

                    humidity=hour.get("humidity"),

                    wind_speed=hour.get("windspeed")

                )

            )

            count += 1

    return standard_weather_structure(

        provider="VisualCrossing",

        latitude=lat,

        longitude=lon,

        forecast=forecast

    )