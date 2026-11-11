from providers.utils import (
    standard_weather_structure
)


def fetch_imd(lat, lon):

    forecast = []

    return standard_weather_structure(
        "IMD",
        lat,
        lon,
        forecast
    )