# app.py
import streamlit as st
import requests
from datetime import datetime, timedelta

def gauti_kritulius():
    url = "https://eismoinfo.lt/eismoinfo-backend/osi-info-table/55?pageNumber=0&pageSize=1000000"
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        return f"Klaida jungiantis prie API: {e}"

    if response.status_code != 200:
        return f"Klaida jungiantis prie API. Statusas: {response.status_code}"

    data = response.json()
    info = data.get("info", [])

    lt_offset = timedelta(hours=3)
    today_lt = (datetime.utcnow() + lt_offset).date()

    total = 0.0
    for item in info:
        timestamp_ms = item.get("date")
        intensity = item.get("precipitationIntensity")
        if timestamp_ms is None or intensity is None:
            continue
        dt_utc = datetime.utcfromtimestamp(timestamp_ms / 1000)
        dt_lt = dt_utc + lt_offset
        if dt_lt.date() == today_lt and intensity > 0:
            total += intensity * 0.25

    total = round(total, 2)
    return f"Šiandien ({today_lt}) iškritusių kritulių kiekis: {total} mm\nIš viso įrašų: {len(info)}"

# Streamlit UI
st.set_page_config(page_title="Kritulių skaičiuoklė")
st.title("🌧️ Lietuvos kritulių kiekis šiandien")
st.write(gauti_kritulius())
