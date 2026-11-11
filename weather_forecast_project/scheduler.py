import schedule
import time
from main import run_pipeline


schedule.every().day.at("09:00")

print("Scheduler started...")
print("Daily run time: 09:15 AM IST")

while True:
    schedule.run_pending()
    time.sleep(60)