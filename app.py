import pandas as pd
import folium
import pydeck
import streamlit as st
import numpy as np
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

df = pd.read_excel('scraping_kosan.xlsx')
polygon = pd.read_excel('kordinat_polygon.xlsx')

#peta
center_lat = -6.8907
center_lon = 107.542
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)


st.title('ANALISIS DAN REKOMENDASI PENETAPAN HARGA KOS DI BERBAGAI AREA')
st.write('Hasil analisis kelompok kami, akan memberikan informasi kepada ' \
'wirausaha yang ingin membangun kos-kosan, berapa harga yang tepat serta berapa fasilitas yang perlu diberikan di setiap areanya.')

#marker
for idx, row in df.iterrows():
    if str(row['Kota']).strip().lower() == 'tangerang':
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=(
                f"Kota: {row['Kota']}<br>"
                f"Latitude: {row['Latitude']}<br>"
                f"Longitude: {row['Longitude']}"
            ),
            tooltip="Klik untuk info"
        ).add_to(m)

for kota, group in polygon.groupby("Kota"):

    coords = group[["Latitude", "Longitude"]].values.tolist()

    if len(coords) >= 3:
        folium.Polygon(
            locations=coords,
            tooltip=kota,
            popup=f"wilayah {kota}",
            color="red",
            fill=True,
            fill_opacity=0.4
        ).add_to(m)

# Tampilkan peta di Streamlit
st.title("Peta Kosan")
st_folium(m, width=700, height=500)