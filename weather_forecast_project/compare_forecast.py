import pandas as pd
import json
import glob
import os

# -------------------------------
# FIND CSV FILE AUTOMATICALLY
# -------------------------------

csv_files = glob.glob("*.csv")

if len(csv_files) == 0:

    print("No CSV file found")
    exit()

csv_file = csv_files[0]

print(f"\nUsing CSV File: {csv_file}")

# -------------------------------
# LOAD ACTUAL SENSOR DATA
# -------------------------------

actual_df = pd.read_csv(csv_file)

# Clean column names
actual_df.columns = actual_df.columns.str.strip()

print("\nAVAILABLE COLUMNS:")
print(actual_df.columns)

# -------------------------------
# FIND JSON FORECAST FILES
# -------------------------------

json_files = glob.glob(
    "storage/**/*.json",
    recursive=True
)

if len(json_files) == 0:

    print("No forecast JSON files found")
    exit()

# Use first JSON file
forecast_file = json_files[0]

print(f"\nUsing Forecast File: {forecast_file}")

# -------------------------------
# LOAD FORECAST JSON
# -------------------------------

with open(forecast_file, "r") as f:

    forecast_json = json.load(f)

forecast_df = pd.DataFrame(
    forecast_json["forecast"]
)

# -------------------------------
# CONVERT TIMESTAMPS
# -------------------------------

forecast_df["timestamp"] = pd.to_datetime(
    forecast_df["timestamp"]
)

actual_df["server_time_stamp"] = pd.to_datetime(
    actual_df["server_time_stamp"]
)

# -------------------------------
# SORT DATA
# -------------------------------

forecast_df = forecast_df.sort_values(
    "timestamp"
)

actual_df = actual_df.sort_values(
    "server_time_stamp"
)

# -------------------------------
# DEVICE ID COLUMN
# -------------------------------

device_column = None

possible_columns = [
    "DEVICE_ID",
    "device_id",
    "station_id",
    "sensor_id"
]

for col in possible_columns:

    if col in actual_df.columns:

        device_column = col
        break

if device_column is None:

    print("\nNo device ID column found")
    exit()

# -------------------------------
# SELECT FIRST DEVICE
# -------------------------------

device_id = actual_df[
    device_column
].iloc[0]

device_actual = actual_df[
    actual_df[device_column] == device_id
]

print("\n===================================")
print(f"DEVICE ID: {device_id}")
print("===================================\n")

# -------------------------------
# COMPARE DATA
# -------------------------------

rows = min(
    5,
    len(forecast_df),
    len(device_actual)
)

for i in range(rows):

    forecast_row = forecast_df.iloc[i]

    actual_row = device_actual.iloc[i]

    print("TIMESTAMP")
    print("Forecast :", forecast_row["timestamp"])
    print("Actual   :", actual_row["server_time_stamp"])

    print("\nTEMPERATURE")
    print("Forecast :", forecast_row.get("temperature_c"))
    print("Actual   :", actual_row.get("TEMPERATURE"))

    print("\nHUMIDITY")
    print("Forecast :", forecast_row.get("humidity_percent"))
    print("Actual   :", actual_row.get("HUMIDITY"))

    print("\nRAINFALL")
    print("Forecast :", forecast_row.get("rainfall_mm"))
    print("Actual   :", actual_row.get("RAINFALL_1HR"))

    print("\n===================================\n")