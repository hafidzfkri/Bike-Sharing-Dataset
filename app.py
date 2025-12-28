import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set_style("whitegrid")

@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear/Few clouds",
        2: "Mist/Cloudy",
        3: "Light snow/rain",
        4: "Heavy rain/snow",
    }

    day_df["season_name"] = day_df["season"].map(season_map)
    day_df["weather_name"] = day_df["weathersit"].map(weather_map)
    hour_df["season_name"] = hour_df["season"].map(season_map)
    hour_df["weather_name"] = hour_df["weathersit"].map(weather_map)

    day_df["year"] = day_df["yr"].map({0: 2011, 1: 2012})
    hour_df["year"] = hour_df["yr"].map({0: 2011, 1: 2012})

    return day_df, hour_df

day_df, hour_df = load_data()

st.title("Bike Sharing Dashboard")
st.caption("Ringkasan analisis dari notebook: jam puncak (workingday vs non-workingday) dan pengaruh cuaca & musim.")

# ========== Sidebar Filter ==========
st.sidebar.header("Filter")

year_options = sorted(day_df["year"].unique().tolist())
selected_year = st.sidebar.multiselect("Tahun", year_options, default=year_options)

day_f = day_df[day_df["year"].isin(selected_year)].copy()
hour_f = hour_df[hour_df["year"].isin(selected_year)].copy()

# ========== KPI ==========
total_cnt = int(day_f["cnt"].sum())
avg_daily = float(day_f["cnt"].mean()) if len(day_f) else 0.0
registered_ratio = float(day_f["registered"].sum() / day_f["cnt"].sum()) if day_f["cnt"].sum() != 0 else 0.0

c1, c2, c3 = st.columns(3)
c1.metric("Total Rental", f"{total_cnt:,}")
c2.metric("Rata-rata Rental Harian", f"{avg_daily:,.0f}")
c3.metric("Registered (%)", f"{registered_ratio*100:.2f}%")

st.divider()

# ========== Pertanyaan 1 ==========
st.subheader("Pertanyaan 1: Jam Puncak & Workingday vs Non-workingday")

left, right = st.columns(2)

with left:
    avg_hour = hour_f.groupby("hr")["cnt"].mean().reset_index()
    fig1 = plt.figure(figsize=(8,4))
    sns.lineplot(data=avg_hour, x="hr", y="cnt", marker="o")
    plt.title("Rata-rata Rental per Jam (Overall)")
    plt.xlabel("Jam")
    plt.ylabel("Rata-rata cnt")
    plt.xticks(range(0,24))
    st.pyplot(fig1)

with right:
    pivot = hour_f.pivot_table(values="cnt", index="hr", columns="workingday", aggfunc="mean")
    if 0 not in pivot.columns:
        pivot[0] = np.nan
    if 1 not in pivot.columns:
        pivot[1] = np.nan
    pivot = pivot.sort_index()

    fig2 = plt.figure(figsize=(8,4))
    plt.plot(pivot.index, pivot[0], marker="o", label="Non-workingday")
    plt.plot(pivot.index, pivot[1], marker="o", label="Workingday")
    plt.title("Perbandingan per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Rata-rata cnt")
    plt.xticks(range(0,24))
    plt.legend()
    st.pyplot(fig2)

top5 = hour_f.groupby("hr")["cnt"].mean().sort_values(ascending=False).head(5)
st.write("Top 5 jam puncak (overall):")
st.dataframe(top5)

st.divider()

# ========== Pertanyaan 2 ==========
st.subheader("Pertanyaan 2: Pengaruh Cuaca & Musim")

wcol, scol = st.columns(2)

with wcol:
    weather_mean = day_f.groupby("weather_name")["cnt"].mean().sort_values(ascending=False)
    fig3 = plt.figure(figsize=(8,4))
    sns.barplot(x=weather_mean.index, y=weather_mean.values)
    plt.title("Rata-rata Rental berdasarkan Cuaca")
    plt.xlabel("Cuaca")
    plt.ylabel("Rata-rata cnt")
    plt.xticks(rotation=15)
    st.pyplot(fig3)

with scol:
    season_mean = day_f.groupby("season_name")["cnt"].mean().sort_values(ascending=False)
    fig4 = plt.figure(figsize=(8,4))
    sns.barplot(x=season_mean.index, y=season_mean.values)
    plt.title("Rata-rata Rental berdasarkan Musim")
    plt.xlabel("Musim")
    plt.ylabel("Rata-rata cnt")
    st.pyplot(fig4)

st.divider()

# ========== Ringkasan Insight ==========
st.subheader("Ringkasan Insight")
st.markdown("""
- Jam puncak rental cenderung terjadi pada jam commuting (pagi & sore).
- Workingday memiliki pola puncak lebih tajam dibanding non-workingday.
- Cuaca cerah menghasilkan rata-rata rental lebih tinggi, sedangkan cuaca buruk menurunkan demand.
- Musim memengaruhi fluktuasi rental sepanjang tahun.
""")

