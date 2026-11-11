from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["weather_forecast_db"]

collection = db["forecasts"]

print("MongoDB Connected")