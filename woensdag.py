import os
import requests
import json
from datetime import datetime, timedelta

# Secrets uit de environment (voor GitHub Actions)
AUTHORIZATION = os.environ.get("AUTHORIZATION")
LISA_AUTH_TOKEN = os.environ.get("LISA_AUTH_TOKEN")

# Bepaal nu het volgende woensdag-tijdstip om 21:30 (CEST)
now = datetime.now()

# Maandag = 0, woensdag = 2
days_until_wednesday = (2 - now.weekday() + 7) % 7
if days_until_wednesday == 0:
    days_until_wednesday = 7  # Altijd "volgende" woensdag

# Bepaal woensdag erop
next_wednesday = now + timedelta(days=days_until_wednesday)
start_local = next_wednesday.replace(hour=21, minute=30, second=0, microsecond=0)

# Zet CEST om naar UTC (CEST = UTC+2)
start_utc = start_local - timedelta(hours=2)
start_at_iso = start_utc.isoformat() + "Z"

print(f"Maak reservering voor woensdag {start_local.strftime('%Y-%m-%d %H:%M')} CEST")

url = "https://api.knltb.club/v1/pub/tennis/clubs/ce59c434-e1d2-4157-9182-991b3d5ea7ad/reservations"

headers = {
    "Content-Type": "application/json",
    "Authorization": AUTHORIZATION,
    "x-lisa-auth-token": LISA_AUTH_TOKEN,
    "Accept": "*/*",
    "User-Agent": "KNLTB/202503280924 CFNetwork/1382.500.131 Darwin/24.5.0",
    "Connection": "keep-alive"
}

court_ids = [
    "8a708d2b-9469-40f2-8488-f26727df9c5e",  # Baan 1
    "18fe2f95-5085-466f-9d9e-b6bc170a955e",  # Baan 2
    "b2d1b949-6280-46a4-944b-7ae5d458e174",  # Baan 3
]

for court_id in court_ids:
    data = {
        "reservation": {
            "club_member_ids": [
                "67e932e5-b11e-4668-8c98-d7293315d637",
                "63033fd9-e999-4455-b822-5bd30d86f6d4",
                "eeb2808c-d33d-4790-8a51-98a9fe6cbd26",
                "2d98b9d1-c1f2-4bd4-ac58-e0e8453f0d49"
            ],
            "court_id": court_id,
            "products": [],
            "callback_url": "https://betalingen.knltb.club/AppCustomPages/redirectButton/tennis",
            "guests": [],
            "start_at": start_at_iso
        }
    }

    print(f"Probeer reservering op court: {court_id}")
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print("Statuscode:", response.status_code)
    if response.status_code == 201:
        print("✅ Succesvolle reservering op deze baan!")
        print(response.text)
        break
    else:
        print("Niet gelukt, probeer volgende baan...")
        print(response.text)
