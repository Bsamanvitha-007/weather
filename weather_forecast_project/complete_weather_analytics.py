import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

from pymongo import MongoClient

# =====================================================
# CONNECT TO MONGODB
# =====================================================

client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["weather_forecast_db"]

collection = db["forecasts"]

print("MongoDB Connected")

# =====================================================
# PARAMETERS
# =====================================================

parameters = {

    "TEMPERATURE": "temperature_c",

    "HUMIDITY": "humidity_percent",

    "RAINFALL_PER_HR": "rainfall_mm",

    "WIND_VELOCITY": "wind_speed",

    "WIND_DIRECTION": "wind_direction_deg"

}

# =====================================================
# CREATE GRAPHS FOLDER
# =====================================================

os.makedirs(
    "graphs",
    exist_ok=True
)

# =====================================================
# MAE FUNCTION
# =====================================================

def calculate_mae(actual, forecast):

    actual = pd.to_numeric(
        actual,
        errors="coerce"
    )

    forecast = pd.to_numeric(
        forecast,
        errors="coerce"
    )

    diff = (actual - forecast).abs()

    return diff.mean()

# =====================================================
# GET CSV FILES
# =====================================================

csv_files = glob.glob(
    "actual_data/*.csv"
)

if len(csv_files) == 0:

    print("No CSV files found")

    exit()

# =====================================================
# PROCESS EACH CSV
# =====================================================

for csv_file in csv_files:

    print("\n================================================")
    print(f"Processing {csv_file}")

    # =================================================
    # DEVICE ID
    # =================================================

    filename = os.path.basename(csv_file)

    parts = filename.split("_")

    device_id = parts[4]

    print(f"Device ID: {device_id}")

    # =================================================
    # LOAD ACTUAL DATA
    # =================================================

    actual_df = pd.read_csv(csv_file)

    actual_df.columns = (

        actual_df.columns
        .str.strip()
        .str.upper()

    )

    # =================================================
    # CHECK TIMESTAMP COLUMN
    # =================================================

    if "SERVER_TIME_STAMP" not in actual_df.columns:

        print("SERVER_TIME_STAMP column missing")
        continue

    # =================================================
    # CONVERT TIMESTAMP
    # =================================================

    actual_df["SERVER_TIME_STAMP"] = pd.to_datetime(

        actual_df["SERVER_TIME_STAMP"],

        errors="coerce"

    ).dt.tz_localize(None)

    # ROUND TO HOUR

    actual_df["MATCH_TIME"] = (

        actual_df["SERVER_TIME_STAMP"]

        .dt.floor("h")

    )

    # =================================================
    # PARAMETERS LOOP
    # =================================================

    for actual_column, forecast_column in parameters.items():

        print("\n----------------------------------------")
        print(f"Generating {actual_column}")

        if actual_column not in actual_df.columns:

            print(f"{actual_column} missing")
            continue

        # =============================================
        # CREATE GRAPH
        # =============================================

        plt.figure(figsize=(16, 8))

        # =============================================
        # PLOT ACTUAL
        # =============================================

        plt.plot(

            actual_df["MATCH_TIME"],

            actual_df[actual_column],

            label="Actual Data",

            linewidth=3

        )

        # =============================================
        # GET PROVIDERS
        # =============================================

        providers = collection.distinct(
            "provider"
        )

        provider_scores = []

        colors = [

            "red",
            "green",
            "blue",
            "orange",
            "purple",
            "brown",
            "pink",
            "cyan",
            "black"

        ]

        color_index = 0

        # =============================================
        # EACH PROVIDER
        # =============================================

        for provider in providers:

            print(f"Checking {provider}")

            # =========================================
            # GET DOCUMENT
            # =========================================

            document = collection.find_one(

                {
                    "provider": provider
                },

                sort=[("_id", -1)]

            )

            if not document:

                print(f"No document for {provider}")
                continue

            # =========================================
            # FORECAST CHECK
            # =========================================

            if "forecast" not in document:

                print(f"No forecast in {provider}")
                continue

            forecast_data = document["forecast"]

            if len(forecast_data) == 0:

                print(f"Empty forecast for {provider}")
                continue

            # =========================================
            # CREATE DATAFRAME
            # =========================================

            forecast_df = pd.DataFrame(
                forecast_data
            )

            # =========================================
            # COLUMN CHECK
            # =========================================

            if forecast_column not in forecast_df.columns:

                print(
                    f"{forecast_column} missing in {provider}"
                )

                continue

            if "timestamp" not in forecast_df.columns:

                print(f"No timestamp in {provider}")
                continue

            # =========================================
            # CONVERT TIMESTAMP
            # =========================================

            forecast_df["timestamp"] = pd.to_datetime(

                forecast_df["timestamp"],

                errors="coerce",

                utc=True

            ).dt.tz_localize(None)

            # ROUND TO HOUR

            forecast_df["MATCH_TIME"] = (

                forecast_df["timestamp"]

                .dt.floor("h")

            )

            # =========================================
            # DROP NULLS
            # =========================================

            forecast_df = forecast_df.dropna(

                subset=["MATCH_TIME"]

            )

            # =========================================
            # MERGE
            # =========================================

            merged = pd.merge(

                actual_df,

                forecast_df,

                on="MATCH_TIME",

                how="inner"

            )

            if len(merged) == 0:

                print(
                    f"No matching timestamps for {provider}"
                )

                continue

            # =========================================
            # MAE
            # =========================================

            mae = calculate_mae(

                merged[actual_column],

                merged[forecast_column]

            )

            provider_scores.append({

                "provider": provider,

                "mae": round(mae, 3)

            })

            # =========================================
            # PLOT PROVIDER
            # =========================================

            plt.plot(

                forecast_df["MATCH_TIME"],

                forecast_df[forecast_column],

                label=(
                    f"{provider} "
                    f"(MAE={round(mae, 2)})"
                ),

                color=colors[
                    color_index % len(colors)
                ]

            )

            color_index += 1

        # =============================================
        # BEST PROVIDER
        # =============================================

        if len(provider_scores) == 0:

            print("No provider data available")

            plt.close()

            continue

        provider_scores = sorted(

            provider_scores,

            key=lambda x: x["mae"]

        )

        best_provider = provider_scores[0]["provider"]

        best_mae = provider_scores[0]["mae"]

        print(
            f"Best Provider: "
            f"{best_provider} "
            f"(MAE={best_mae})"
        )

        # =============================================
        # TITLE
        # =============================================

        plt.title(

            f"{actual_column} Comparison\n"
            f"Best Provider: "
            f"{best_provider} "
            f"(MAE={best_mae})"

        )

        plt.xlabel(
            "Timeline"
        )

        plt.ylabel(
            actual_column
        )

        plt.legend()

        plt.grid(True)

        plt.xticks(rotation=45)

        plt.tight_layout()

        # =============================================
        # SAVE GRAPH
        # =============================================

        output_file = (

            f"graphs/"
            f"{device_id}_{actual_column}.png"

        )

        plt.savefig(output_file)

        print(f"Saved Graph: {output_file}")

        plt.close()

# =====================================================
# COMPLETE
# =====================================================

print("\n================================================")
print("ALL ANALYTICS GRAPHS GENERATED")
print("CHECK graphs FOLDER")
print("================================================")