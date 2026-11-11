from providers.utils import (
    standard_weather_structure
)


def fetch_ibm_twc(lat, lon):

    forecast = []

    return standard_weather_structure(
        "IBM_TWC",
        lat,
        lon,
        forecast
    )