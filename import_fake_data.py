import pandas as pd
from faker import Faker
import random

fake = Faker()

positions = ["AI Engineer", "Software Engineer", "Data Scientist", "Content Writer", "DevOps Engineer"]
application_statuses = ["Pending", "Reviewed", "Rejected"]
interview_statuses = ["Scheduled", "Completed"]
modes = ["Online", "On-site"]
addresses = [
    "https://zoom.us/j/123456789",
    "https://meet.google.com/abc-defg-hij",
    "123 Office St, Karachi",
    "Suite 22, Blue Area, Islamabad"
]

data = []

for _ in range(200):
    name = fake.name()
    position = random.choice(positions)
    app_date = fake.date_between(start_date="-30d", end_date="today").strftime("%Y-%m-%d")
    app_status = random.choice(application_statuses)

    if app_status in ["Pending", "Rejected"]:
        interview_status = "-"
        interview_date = "-"
        interview_time = "-"
        interview_mode = "-"
        interview_address = "-"
    else:
        interview_status = random.choice(interview_statuses)
        interview_date = fake.date_between(start_date="today", end_date="+15d").strftime("%Y-%m-%d")
        interview_time = fake.time()
        interview_mode = random.choice(modes)
        interview_address = random.choice(addresses)

    data.append({
        "Name": name,
        "Position": position,
        "Application Date": app_date,
        "Application Status": app_status,
        "Interview Status": interview_status,
        "Interview Date": interview_date,
        "Interview Time": interview_time,
        "Interview Mode": interview_mode,
        "Address": interview_address
    })

df = pd.DataFrame(data)
df.to_csv("applications.csv", index=False)
print("Data has been saved.")
