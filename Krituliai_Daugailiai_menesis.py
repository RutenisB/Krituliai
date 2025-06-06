import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Nustatymai
st.set_page_config(page_title="Kritulių grafikas")
st.title("🌧️ Kritulių kiekis Daugailiuose – mėnesio grafikas")

# Gauti duomenis
url = "https://eismoinfo.lt/eismoinfo-backend/osi-info-table/55?pageNumber=0&pageSize=1000000"
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"Klaida gaunant duomenis: {e}")
    st.stop()

info = data.get("info", [])

# Laiko poslinkis
lt_offset = timedelta(hours=3)

# Sukuriam DataFrame su datomis ir intensyvumu
rows = []
for item in info:
    timestamp_ms = item.get("date")
    intensity = item.get("precipitationIntensity")

    if timestamp_ms is None or intensity is None:
        continue

    dt_utc = datetime.utcfromtimestamp(timestamp_ms / 1000)
    dt_lt = dt_utc + lt_offset

    rows.append({
        "date": dt_lt.date(),
        "intensity": intensity * 0.25  # 15 min -> mm
    })

df = pd.DataFrame(rows)

# Filtruojam tik einamą mėnesį
today = datetime.utcnow() + lt_offset
df = df[df["date"].between(today.replace(day=1).date(), today.date())]

# Grupavimas pagal dieną
daily = df.groupby("date").sum().reset_index()

# Atvaizduojam grafike
fig, ax = plt.subplots()
bars = ax.bar(daily["date"].astype(str), daily["intensity"], color='skyblue')
ax.set_title(f"Kritulių kiekis per {today.strftime('%B')} mėnesį")
ax.set_xlabel("Diena")
ax.set_ylabel("Krituliai (mm)")
plt.xticks(rotation=0)

# Pridedam stulpelių reikšmes virš jų
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
            ha='center', va='bottom', fontsize=8, rotation=90)

st.pyplot(fig)
