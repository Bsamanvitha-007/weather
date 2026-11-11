from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["weather_forecast_db"]
collection = db["forecasts"]

providers = collection.distinct("provider")

print("\nPROVIDER STATUS\n")

for provider in providers:

    doc = collection.find_one(
        {"provider": provider},
        sort=[("_id", -1)]
    )

    if not doc:
        print(f"{provider}: NO DATA")
        continue

    forecast = doc.get("forecast", [])

    print(
        f"{provider}: "
        f"{len(forecast)} forecast records"
    )