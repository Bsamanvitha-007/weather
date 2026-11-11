# providers/utils.py

from datetime import datetime


def standard_weather_structure(
    provider,
    latitude,
    longitude,
    forecast
):

    return {

        "provider": provider,

        "latitude": latitude,

        "longitude": longitude,

        "forecast": forecast

    }


def build_forecast_entry(
    timestamp,
    rainfall=None,
    temperature=None,
    humidity=None,
    wind_speed=None,
    wind_direction=None,
    pressure=None,
    cloud_cover=None
):
    return {
        "timestamp": timestamp,
        "rainfall_mm": rainfall,
        "temperature_c": temperature,
        "humidity_percent": humidity,
        "wind_speed_mps": wind_speed,
        "wind_direction_deg": wind_direction,
        "pressure_hpa": pressure,
        "cloud_cover_percent": cloud_cover
    }