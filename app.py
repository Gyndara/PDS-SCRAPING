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
center_lat_bandung = -6.924022570852051 
center_lon_bandung = 107.68061945673925

m = folium.Map(location=[center_lat_bandung, center_lon_bandung], zoom_start=12)

st.title('ANALISIS DAN REKOMENDASI HARGA KOSAN BERDASARKAN PERSEBARAN KOSAN RUKITA')
st.write('Hasil analisis kelompok kami, akan memberikan informasi kepada ' \
'wirausaha yang ingin membangun kos-kosan, area mana yang belum padat pembangunan kos-kosan, berapa harga yang tepat serta berapa fasilitas yang perlu diberikan di setiap areanya.')

jumlah_kosan_per_kota = df["Kota"].value_counts()

gabungan_kota = {
    "Bandung": ["Bandung", "Kabupaten Bandung", 'Kabupaten Bandung Barat'],
    "Yogyakarta": ["Yogyakarta", "Kabupaten Bantul"],
    "Solo (Surakarta)": ["Solo (Surakarta)", "Kabupaten Karanganyar"]
}

for kota, group in polygon.groupby("Kota"):

    coords = group[["Latitude", "Longitude"]].values.tolist()

    #menghitung gabungan kota
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

st.title("Bandung dan sekitarnya")
st_folium(m, width=700, height=500)

center_lat_jakarta = -6.266167987422056
center_lon_jakarta = 106.78322043697327

j = folium.Map(location=[center_lat_jakarta, center_lon_jakarta], zoom_start=10.5)

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
        ).add_to(j)

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        tooltip=kota,
        popup=f"{kota}<br>Jumlah kosan: {jumlah_kosan}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(j)


st.title("Jakarta dan sekitarnya")
st_folium(j, width=700, height=500)


center_lat_bogor = -6.546766181363673
center_lon_bogor = 106.82582503678688

b = folium.Map(location=[center_lat_bogor, center_lon_bogor], zoom_start=12)

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
        ).add_to(b)

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        tooltip=kota,
        popup=f"{kota}<br>Jumlah kosan: {jumlah_kosan}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(b)


st.title('Bogor')
st_folium(b, width=700, height=500)

center_lat_yogya = -7.738462636007786 
center_lon_yogya = 110.3976623661559

y = folium.Map(location=[center_lat_yogya, center_lon_yogya], zoom_start=12)

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
        ).add_to(y)

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        tooltip=kota,
        popup=f"{kota}<br>Jumlah kosan: {jumlah_kosan}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(y)


st.title('Yogyakarta dan Kabupaten Sleman')
st_folium(y, width=700, height=500)


center_lat_semarang = -7.001714208585145 
center_lon_semarang = 110.3976623661559

s = folium.Map(location=[center_lat_semarang, center_lon_semarang], zoom_start=12)

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
        ).add_to(s)

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        tooltip=kota,
        popup=f"{kota}<br>Jumlah kosan: {jumlah_kosan}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(s)


st.title('Semarang')
st_folium(s, width=700, height=500)