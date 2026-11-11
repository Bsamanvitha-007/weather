import pandas as pd
import os
import json
from datetime import datetime
from mongodb import collection
from providers.openmeteo_provider import fetch_openmeteo
from providers.openweather_provider import fetch_openweather
from providers.tomorrow_provider import fetch_tomorrow
from providers.ecmwf_provider import fetch_ecmwf
from providers.meteomatics_provider import fetch_meteomatics
from providers.ibm_twc_provider import fetch_ibm_twc
from providers.imd_provider import fetch_imd
from providers.visualcrossing_provider import fetch_visualcrossing
from providers.agromonitoring_provider import fetch_agromonitoring


PROVIDERS = {

    "Open-Meteo": fetch_openmeteo,

    "OpenWeatherMap": fetch_openweather,

    "Tomorrow.io": fetch_tomorrow,

    "VisualCrossing": fetch_visualcrossing,

    "Agromonitoring": fetch_agromonitoring,

    "ECMWF": fetch_ecmwf,

    "Meteomatics": fetch_meteomatics,

    "IBM_TWC": fetch_ibm_twc,

    "IMD": fetch_imd
}


def load_locations(file_path):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    valid_locations = []

    for _, row in df.iterrows():

        lat = row["lat"]
        lon = row["lon"]

        if lat == -1 or lon == -1:
            continue

        valid_locations.append((lat, lon))

    return valid_locations


def save_json(provider, lat, lon, data):

    date_folder = datetime.now().strftime("%Y-%m-%d")

    folder = os.path.join(
        "storage",
        date_folder,
        provider
    )

    os.makedirs(folder, exist_ok=True)

    filename = f"{lat}_{lon}.json"

    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:

        json.dump(data, f, indent=4)

    print(f"Saved JSON: {filepath}")
def save_to_mongodb(data):

    collection.insert_one(data)

def run_pipeline():

    locations = load_locations(
        "locations/es_devices_lat_lon.xlsx"
    )

    for lat, lon in locations:

        print(f"Processing {lat}, {lon}")

        for provider, function in PROVIDERS.items():

            try:

                print(f"Fetching from {provider}")

                result = function(lat, lon)
                
                save_json(
                    provider,
                    lat,
                    lon,
                    result
                )
                
                # THEN save to MongoDB
                save_to_mongodb(result)
                print(f"Saved {provider}")

            except Exception as e:

                print(f"Error in {provider}: {e}")


if __name__ == "__main__":

    run_pipeline()