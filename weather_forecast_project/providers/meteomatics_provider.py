import requests

from config import (
    METEOMATICS_USERNAME,
    METEOMATICS_PASSWORD
)

from providers.utils import (
    build_forecast_entry,
    standard_weather_structure
)


def fetch_meteomatics(lat, lon):

    url = (
        f"https://api.meteomatics.com/"
        f"nowP2D:PT1H/"
        f"t_2m:C,"
        f"precip_1h:mm,"
        f"relative_humidity_2m:p,"
        f"wind_speed_10m:ms/"
        f"{lat},{lon}/json"
    )

    response = requests.get(
        url,
        auth=(
            METEOMATICS_USERNAME,
            METEOMATICS_PASSWORD
        )
    )

    data = response.json()

    forecast = []

    try:

        dates = data["data"][0]["coordinates"][0]["dates"]

        for item in dates[:48]:

            forecast.append(
                build_forecast_entry(
                    timestamp=item.get("date"),
                    temperature=item.get("value")
                )
            )

    except Exception as e:

        print("Meteomatics Error:", e)

    return standard_weather_structure(
        "Meteomatics",
        lat,
        lon,
        forecast
    )