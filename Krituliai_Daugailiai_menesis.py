# Grupavimas pagal dieną
daily = df.groupby("date").sum().reset_index()

# Apskaičiuojam bendrą kritulių sumą per mėnesį
total_precipitation = daily["intensity"].sum()

# Atvaizduojam grafike
fig, ax = plt.subplots()
bars = ax.bar(daily["date"].astype(str), daily["intensity"], color='skyblue')
ax.set_title(f"Kritulių kiekis per {today.strftime('%B')} mėnesį")
ax.set_xlabel("Diena")
ax.set_ylabel("Krituliai (mm)")
plt.xticks(rotation=80)

# Pridedam stulpelių reikšmes virš jų
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
            ha='center', va='bottom', fontsize=8, rotation=0)

st.pyplot(fig)

# Išvedam bendrą kritulių kiekį kaip atskirą įrašą po grafiku
st.markdown(f"### 🌧️ Bendra kritulių suma per mėnesį: **{total_precipitation:.2f} mm**")
