import requests
import json
import time
from datetime import datetime, timezone, timedelta

# === CONFIGURATIE ===

# LOKALE tijd waarop je wilt reserveren (CEST = UTC+2)
RESERVEER_OP = "2025-05-19 10:30:01"  # Format: JJJJ-MM-DD HH:MM:SS

AUTHORIZATION = "Basic bGlzYXgtYXBpLXB1Yi11c2VyOjZUNmhyTTBOZTkxQlNqa3ZpSnhoOE1BalNucE4xTTl1"
LISA_AUTH_TOKEN = "N8PDEdj0GaE_XLqXmDZ0zA=="

# === BEREKEN 'start_at' in UTC ===

# Lokaal tijdstip waarop de reservering moet starten (deze keer: 10:30 lokale tijd)
start_local = datetime.strptime("2025-05-19 10:30:00", "%Y-%m-%d %H:%M:%S")

# Zet CEST tijd (UTC+2) om naar UTC
start_utc = start_local - timedelta(hours=2)
start_at_iso = start_utc.isoformat() + "Z"

# === API-instellingen ===

url = "https://api.knltb.club/v1/pub/tennis/clubs/ce59c434-e1d2-4157-9182-991b3d5ea7ad/reservations"

headers = {
    "Content-Type": "application/json",
    "Authorization": AUTHORIZATION,
    "x-lisa-auth-token": LISA_AUTH_TOKEN,
    "Accept": "*/*",
    "Accept-Language": "nl-NL,nl;q=0.9",
    "User-Agent": "KNLTB/202503280924 CFNetwork/1382.500.131 Darwin/24.5.0",
    "Connection": "keep-alive"
}

data = {
    "reservation": {
        "club_member_ids": [
            "67e932e5-b11e-4668-8c98-d7293315d637",
            "63033fd9-e999-4455-b822-5bd30d86f6d4",
            "eeb2808c-d33d-4790-8a51-98a9fe6cbd26",
            "2d98b9d1-c1f2-4bd4-ac58-e0e8453f0d49"
        ],
        "court_id": "8a708d2b-9469-40f2-8488-f26727df9c5e",
        "products": [],
        "callback_url": "https://betalingen.knltb.club/AppCustomPages/redirectButton/tennis",
        "guests": [],
        "start_at": start_at_iso  # Automatisch UTC!
    }
}

# === WACHT TOT MOMENT VAN RESERVEREN ===

doel = datetime.strptime(RESERVEER_OP, "%Y-%m-%d %H:%M:%S").timestamp()
print(f"Wachten tot {RESERVEER_OP} (CEST)...")

while time.time() < doel:
    time.sleep(0.1)

# === VERSTUUR RESERVERING ===

print("Reservering verzenden...")
response = requests.post(url, headers=headers, data=json.dumps(data))

print("Statuscode:", response.status_code)
print("Antwoord:", response.text)
