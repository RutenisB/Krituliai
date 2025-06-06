import requests
from datetime import datetime, timedelta

# API nuoroda
url = "https://eismoinfo.lt/eismoinfo-backend/osi-info-table/55?pageNumber=0&pageSize=1000000"
response = requests.get(url)

# Patikrinam ar užklausa pavyko
if response.status_code == 200:
    data = response.json()
    info = data.get("info", [])

    # Laiko zona: Lietuva (UTC+3 vasarą)
    lt_offset = timedelta(hours=3)
    today_lt = (datetime.utcnow() + lt_offset).date()

    # Skaičiuojam bendrą kritulių kiekį tik iš šiandienos
    total_precipitation = 0.0
    for item in info:
        timestamp_ms = item.get("date")
        intensity = item.get("precipitationIntensity")

        if timestamp_ms is None or intensity is None:
            continue

        # Konvertuojam laiką į LT laiką
        dt_utc = datetime.utcfromtimestamp(timestamp_ms / 1000)
        dt_lt = dt_utc + lt_offset

        # Tikrinam ar tai šiandienos įrašas
        if dt_lt.date() == today_lt and intensity > 0:
            total_precipitation += intensity * 0.25  # 15 minučių = 0.25 val.

    # Suapvalinam
    total_precipitation = round(total_precipitation, 2)

    # Išvedam rezultatą
    print(f"Įrašų kiekis: {len(info)}")
    print(f"Šiandienos ({today_lt}) bendras kritulių kiekis: {total_precipitation} mm")

else:
    print(f"Klaida jungiantis prie API. Statusas: {response.status_code}")
