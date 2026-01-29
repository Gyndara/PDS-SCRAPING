import pandas as pd
import folium
import pydeck
import streamlit as st
import numpy as np
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

df = pd.read_excel('data/scraping_kosan.xlsx')
polygon = pd.read_excel('data/kordinat_polygon.xlsx')

#peta
center_lat = -6.8907
center_lon = 107.542
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)


st.title('ANALISIS DAN REKOMENDASI HARGA KOSAN BERDASARKAN PERSEBARAN KOSAN RUKITA')
st.write('Hasil analisis kelompok kami, akan memberikan informasi kepada ' \
'wirausaha yang ingin membangun kos-kosan, area mana yang belum padat pembangunan kos-kosan, berapa harga yang tepat serta berapa fasilitas yang perlu diberikan di setiap areanya.')

jumlah_kosan_per_kota = df["Kota"].value_counts()

gabungan_kota = {
    "Bandung": ["Bandung", "Kabupaten Bandung"],
    "Yogyakarta": ["Yogyakarta", "Kabupaten Bantul"],
    "Solo (Surakarta)": ["Solo (Surakarta)", "Kabupaten Karanganyar"]
}

for kota, group in polygon.groupby("Kota"):

    coords = group[["Latitude", "Longitude"]].values.tolist()

    if kota in gabungan_kota:
        jumlah_kosan = sum(
            jumlah_kosan_per_kota.get(k, 0)
            for k in gabungan_kota[kota]
        )
    else:
        jumlah_kosan = jumlah_kosan_per_kota.get(kota, 0)

    if (jumlah_kosan <= 50):
        polygon_color = "yellow"
    elif (jumlah_kosan <= 80):
        polygon_color = "orange"
    elif (jumlah_kosan <= 150):
        polygon_color = "red"
    else:
        polygon_color = "blue"

    if len(coords) >= 3:
        folium.Polygon(
            locations=coords,
            color=polygon_color,
            fill=True,
            fill_color=polygon_color,
            fill_opacity=0.4
        ).add_to(m)

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        tooltip=kota,
        popup=f"{kota}<br>Jumlah kosan: {jumlah_kosan}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Tampilkan peta di Streamlit
st.title("Peta Kosan")
st_folium(m, width=700, height=500)