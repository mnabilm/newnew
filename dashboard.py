import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

sns.set(style='dark')

# Fungsi untuk memproses data
def create_seasonal_rentals_df(df):
    return df.groupby("season")["cnt"].sum().reset_index()

def create_hourly_rentals_df(df):
    return df.groupby("hr")["cnt"].sum().reset_index()

def create_weather_rentals_df(df):
    return df.groupby("weathersit")["cnt"].sum().reset_index()

# Menentukan path dataset secara dinamis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DAYS_PATH = os.path.join(BASE_DIR, "days_df_clean.csv")
HOURS_PATH = os.path.join(BASE_DIR, "hours_df_clean.csv")

# Memuat dataset dengan error handling
try:
    days_df = pd.read_csv(DAYS_PATH)
    hours_df = pd.read_csv(HOURS_PATH)
except FileNotFoundError as e:
    st.error(f"❌ File dataset tidak ditemukan! Pastikan file berada di folder yang sama dengan script ini.")
    st.stop()

# Mengubah tipe data datetime
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Sidebar dengan logo dan filter
st.sidebar.image("https://i.pinimg.com/736x/c6/50/f4/c650f4e5ccd180f4939787d899e17ecd.jpg", width=150)
st.sidebar.header("Filter Data")
season_filter = st.sidebar.multiselect("Pilih Musim:", days_df["season"].unique())
filtered_df = days_df[days_df["season"].isin(season_filter)] if season_filter else days_df

# Memproses data untuk visualisasi
seasonal_rentals_df = create_seasonal_rentals_df(filtered_df)
hourly_rentals_df = create_hourly_rentals_df(hours_df)
weather_rentals_df = create_weather_rentals_df(filtered_df)

# Dashboard
st.title("📊 Dashboard Analisis Data Bike Sharing")

# Visualisasi: Total Peminjaman Berdasarkan Musim
st.subheader("🚴‍♂️ Total Peminjaman Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="season", y="cnt", data=seasonal_rentals_df, ax=ax, estimator=sum)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: int(x)))
st.pyplot(fig)

# Visualisasi: Tren Peminjaman Berdasarkan Jam
st.subheader("🕒 Tren Peminjaman Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x="hr", y="cnt", data=hourly_rentals_df, ax=ax, marker="o")
ax.set_xlabel("Jam")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Tren Peminjaman Sepeda Berdasarkan Jam")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: int(x)))
st.pyplot(fig)

# Visualisasi: Pengaruh Cuaca terhadap Peminjaman
st.subheader("🌤️ Pengaruh Cuaca terhadap Jumlah Peminjaman")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="weathersit", y="cnt", data=weather_rentals_df, ax=ax, estimator=sum)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Pengaruh Cuaca terhadap Peminjaman")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: int(x)))
st.pyplot(fig)

st.caption('Copyright (c) nbl 2025')
