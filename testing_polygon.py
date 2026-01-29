import folium
import streamlit as st
from streamlit_folium import st_folium

# Titik-titik polygon Jakarta Barat (contoh kasar)
polygon_coords = [
    [-6.113665440336424, 106.13523797443428],
    [-6.11847161403225, 106.17758324713942],
    [-6.189108903099577, 106.1201782053762],
    [-6.113665440336424, 106.13523797443428],
]

# Buat peta di sekitar Jakarta Barat
center_lat = -6.205
center_lon = 106.791
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Tambahkan polygon
folium.Polygon(
    locations=polygon_coords,
    color='blue',
    fill=True,
    fill_opacity=0.4,
    popup="Jakarta Barat"
).add_to(m)

# Tampilkan peta di Streamlit
st.title("Polygon Jakarta Barat")
st_folium(m, width=700, height=500)
