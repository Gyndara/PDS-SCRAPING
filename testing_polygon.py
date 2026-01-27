import folium
import streamlit as st
from streamlit_folium import st_folium

# Titik-titik polygon Jakarta Barat (contoh kasar)
jakbar_coords = [
    [-6.919239750595748, 107.61433735217793],  # Titik A
    [-6.92477779834789, 107.593350746215],  # Titik B
    [-6.925978136122512, 107.57455641192054],  # Titik C
    [-6.948427385040432, 107.56236550706024],  # Titik D
    [-6.948077990632563, 107.57305596980642],  # Titik E
    [-6.952157941934111, 107.59557006399424],  # Titik F
    [-6.95574815013219, 107.624537688342],  # Titik G
    [-6.933831193537474, 107.62026020842468],  # Titik H
    [-6.92921616004598, 107.622249398148],  # Titik I
    [-6.919239750595748, 107.61433735217793]
]

bandung_atas = [
    [-6.862129143625276, 107.60483318772368],
    [-6.8753076731146, 107.579654895729],
    [-6.88309844088035, 107.57788821287149],
    [-6.886381483792042, 107.57877550941215],
    [],
    [],
    [],
    [],
    [],
    [],
    [-6.862129143625276, 107.60483318772368]

]

# Buat peta di sekitar Jakarta Barat
center_lat = -6.205
center_lon = 106.791
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Tambahkan polygon
folium.Polygon(
    locations=jakbar_coords,
    color='blue',
    fill=True,
    fill_opacity=0.4,
    popup="Jakarta Barat"
).add_to(m)

# Tampilkan peta di Streamlit
st.title("Polygon Jakarta Barat")
st_folium(m, width=700, height=500)
