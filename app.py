import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

df = pd.read_excel('data/scraping_kosan.xlsx')
polygon = pd.read_excel('data/kordinat_polygon.xlsx')
grafik = pd.read_excel('data/UMR.xlsx')

avg_harga_per_kota = df.groupby("Kota")["Harga (Rp)"].mean().to_dict()
jumlah_kosan_per_kota = df["Kota"].value_counts()

# Gabungan wilayah
gabungan_kota = {
    "Bandung": ["Bandung", "Kabupaten Bandung", "Kabupaten Bandung Barat"],
    "Yogyakarta": ["Yogyakarta", "Kabupaten Bantul"],
    "Solo (Surakarta)": ["Solo (Surakarta)", "Kabupaten Karanganyar"]
}

gabungan_fasilitas = {
    "Bandung": ["Bandung", "Kabupaten Bandung", "Kabupaten Bandung Barat", "Kabupaten Sumedang"],
    "Yogyakarta": ["Yogyakarta", "Kabupaten Sleman"],
    "Solo (Surakarta)": ["Solo (Surakarta)", "Kabupaten Karanganyar"],
    "Jakarta" : ["Kabupaten Tangerang", "Tangerang", "Jakarta Barat", "Jakarta Utara", "Jakarta Pusat", "Jakarta Timur", 
    "Bekasi","Jakarta Selatan", "Tangerang Selatan", "Depok" ],
    "Bogor" : ["Kabupaten Bogor", "Bogor"]
}

# Koordinat awal map
kota_map = {
    '': {'lat': -0.19164045731720974, 'lon': 110.16835376392196, 'zoom': 5},
    'Jakarta': {'lat': -6.2661, 'lon': 106.7832, 'zoom': 10.5},
    'Bandung': {'lat': -6.9240, 'lon': 107.6806, 'zoom': 12},
    'Bogor': {'lat': -6.5467, 'lon': 106.8258, 'zoom': 12},
    'Yogyakarta': {'lat': -7.7384, 'lon': 110.3976, 'zoom': 12},
    'Semarang': {'lat': -7.0017, 'lon': 110.3976, 'zoom': 12},
}

st.title('ANALISIS DAN REKOMENDASI HARGA KOSAN BERDASARKAN PERSEBARAN KOSAN RUKITA')
st.write(
    'Hasil analisis ini memberikan informasi area potensial pembangunan kos, '
    'kepadatan kos, harga rata-rata, serta fasilitas yang tersedia.'
)

selected_city = st.selectbox(
    "Pilih Kota",
    list(kota_map.keys())
)

if selected_city in gabungan_fasilitas:
    df_filtered = df[df["Kota"].isin(gabungan_fasilitas[selected_city])]
    grafik_filtered = grafik[grafik["Kota"].isin(gabungan_fasilitas[selected_city])]
else:
    df_filtered = df[df["Kota"] == selected_city]
    grafik_filtered = grafik[grafik["Kota"] == selected_city]

lat = kota_map[selected_city]['lat']
lon = kota_map[selected_city]['lon']
zoom = kota_map[selected_city]['zoom']

m = folium.Map(location=[lat, lon], zoom_start=zoom)

legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 200px;
    height: 170px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 14px;
    color : black;
    padding: 10px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
<b>Legenda Kepadatan Kosan</b><br><br>
<i style="background:blue; width:18px; height:18px; float:left; margin-right:8px;"></i>
Sangat Rendah (&le; 50)<br>

<i style="background:yellow; width:18px; height:18px; float:left; margin-right:8px;"></i>
Rendah (51–80)<br>

<i style="background:orange; width:18px; height:18px; float:left; margin-right:8px;"></i>
Padat (81–150)<br>

<i style="background:red; width:18px; height:18px; float:left; margin-right:8px;"></i>
Sangat Padat (> 150)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

for kota, group in polygon.groupby("Kota"):

    coords = group[["Latitude", "Longitude"]].values.tolist()

    # hitung kosan gabungan
    if kota in gabungan_kota:
        jumlah_kosan = sum(
            jumlah_kosan_per_kota.get(k, 0)
            for k in gabungan_kota[kota]
        )
    else:
        jumlah_kosan = jumlah_kosan_per_kota.get(kota, 0)

    # warna polygon
    if jumlah_kosan <= 50:
        color = "blue"
    elif jumlah_kosan <= 80:
        color = "yellow"
    elif jumlah_kosan <= 150:
        color = "orange"
    else:
        color = "red"

    if len(coords) >= 3:
        folium.Polygon(
            locations=coords,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.4
        ).add_to(m)

    avg_harga = avg_harga_per_kota.get(kota, 0)

    popup_info = f"""
    <b>{kota}</b><br>
    Jumlah kosan: {jumlah_kosan}<br>
    Rata-rata harga: Rp {avg_harga:,.0f}
    """

    folium.Marker(
        location=[group["Latitude"].mean(), group["Longitude"].mean()],
        popup=popup_info,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

st.subheader(f"Peta Persebaran Kosan – {selected_city}")
st_folium(m, width=700, height=500)


df_tabel_fasilitas = (
    df_filtered
    .groupby("Kota")["Fasilitas"]
    .apply(lambda x: ", ".join(
        sorted(set(", ".join(x.astype(str)).split(", ")))
    ))
    .reset_index()
)

st.subheader(f"Rata-rata fasilitas yang disediakan di area {selected_city}")

st.dataframe(
    df_tabel_fasilitas,
    width="stretch",
    hide_index=True,
)

st.subheader('Grafik perbandingan UMR dengan rata-rata harga kosan')
grafik_filtered = grafik_filtered.copy()

grafik_filtered["Batas 30% UMR"] = grafik_filtered["UMK"] * 0.3
grafik_filtered["Batas 40% UMR"] = grafik_filtered["UMK"] * 0.4
#grafik
plt.figure(figsize=(10, 5))

plt.plot(
    grafik_filtered["Kota"],
    grafik_filtered["UMK"],
    marker="o",
    label="UMR",
    color='green'
)

plt.plot(
    grafik_filtered["Kota"],
    grafik_filtered["ratarata"],
    marker="o",
    label="Rata-rata Harga Kos",
    color='orange'
)

plt.plot(
    grafik_filtered["Kota"],
    grafik_filtered["Batas 30% UMR"],
    marker="o",
    linestyle="--",
    color="blue",
    label="Minimum sewa 30% UMR"
)

plt.plot(
    grafik_filtered["Kota"],
    grafik_filtered["Batas 40% UMR"],
    marker="o",
    linestyle="--",
    color="red",
    label="Maksimum sewa 40% UMR"
)

plt.ylabel("Rupiah (Rp)")
plt.xlabel("Kota")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

st.pyplot(plt)
